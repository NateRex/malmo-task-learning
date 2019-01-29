# ==============================================================================================
# This file represents a standalone script for the post-processing of log files. For each file
# in the logs/ directory, parse the log and resolve any minor issues that have resulted due to
# tolerance issues while the mission ran.
# ==============================================================================================
import os

WORKING_DIR = None          # Current working directory of this script
old_file_contents = []      # A list of the lines for the original log file
new_file_contents = []      # A list of the lines for the new log file after post-processing
id_counters = {}            # A global counter for each type of entity for generating new simple entity ids
id_map = {}                 # A mapping of original complex Malmo ids to simpler ones generated in this script
dead_entities = []          # A list of ids for entities that have been declared as dead
didPassEndMarker = False    # Boolean signifying if we have passed the END marker specifying the start of final state output

def resetGlobals():
    """
    Reset the global values so that they are ready to be used for processing a new log.
    """
    global id_counters, old_file_contents, new_file_contents, id_map, dead_entities, didPassEndMarker
    old_file_contents = []
    new_file_contents = []
    id_counters = {}
    id_map = {}
    dead_entities = []
    didPassEndMarker = False


def getNextIdNumberForType(entityType):
    """
    Returns the next ID number for use for a specific type of entity.
    """
    global id_counters
    if entityType in id_counters:
        id_counters[entityType] += 1
        return id_counters[entityType]
    else:
        id_counters[entityType] = 1
        return 1

def doesLogDirectoryExist():
    """
    Returns true if the output directory containing logs exists. Returns false otherwise.
    """
    logDirPath = os.path.join(WORKING_DIR, "logs")
    if os.path.isdir(logDirPath):
        return True
    else:
        return False

def getLogFilePaths():
    """
    Returns a list of file paths for each log file in the output directory.
    """
    logDirPath = os.path.join(WORKING_DIR, "logs")
    paths = []
    for (dirpath, _, filenames) in os.walk(logDirPath):
        for filename in filenames:
            if filename.endswith(".log"):
                filepath = os.path.join(dirpath, filename)
                paths.append(filepath)
    return paths

def handleEmptyLine(line):
    """
    Handle the case when a line contains the empty string "". Returns true if the line should be appended to the file, false otherwise.
    """
    global new_file_contents
    if len(new_file_contents) > 0:
        if new_file_contents[-1] == "": # No repeated newlines
            return False
        if new_file_contents[-1].startswith("closest"): # No newline after closest_XXX entity output
            return False
    return True

def handleClosestXXXLine(line):
    """
    Handle the case where the line is defining a closest entity to one of the agents. Returns true if the line should be appended to the file, false otherwise.
    """
    global new_file_contents
    if len(new_file_contents) > 0 and new_file_contents[-1].startswith("!"):    # Last action never finished... add a newline before proceeding
        new_file_contents.append("")
    return True

def handleEntityDefinitionLine(line):
    """
    Handle the case where the line is defining a new entity. Returns the new, modified line.
    """
    global id_map
    strings = line.split("-")
    oldEntityId = strings[1]
    entityType = strings[2]
    if oldEntityId in id_map:   # We already defined and simplified this entity id?... shouldn't happen
        strings[1] = id_map[oldEntityId]
    elif oldEntityId == "None": # Special case... do not alter sole member None of NoneType
        id_map["None"] = "None"
    else:
        newEntityId = "{}{}".format(entityType, getNextIdNumberForType(entityType))
        id_map[oldEntityId] = newEntityId
        id_map[newEntityId] = newEntityId
        strings[1] = newEntityId
    return "-".join(strings)
    
def handleEntityStatusLine(line):
    """
    Handle the case where the line is declaring an entity as either alive or dead. Returns true if the line should be appended to the file, false otherwise.
    """
    global dead_entities
    if line.endswith("dead"):
        strings = line.split("-")
        dead_entities.append(strings[1])
    return True

def handleAttackLine(line, lineIdx):
    """
    Handle the case where the line declares an attack on an entity by some agent. This requires the line number that the attack occurred on.
    Returns the amount to move the line index head for reading from the old file contents.
    """
    global new_file_contents
    attackedEntityId = line.split("-")[2]

    targetAttackIdx = None   # Line of attack action that resulted in the entity dying (if any)
    lastAttackIdx = lineIdx  # Line of the last attack in this series of attacks
    for i in range(lineIdx, len(old_file_contents)):
        lineToCheck = old_file_contents[i]
        if not lineToCheck.startswith("!"):
            continue
        else:
            if lineToCheck.startswith("!ATTACK") and lineToCheck.endswith(attackedEntityId):
                lastAttackIdx = i
                nextLine = old_file_contents[i + 1] if i < len(old_file_contents) - 1 else ""
                if nextLine.startswith("status"):
                    targetAttackIdx = i
            else:
                break

    # If this attack ended with the entity dying, make sure it is officially logged and return to move ahead in the log past the status update
    if targetAttackIdx != None:
        statusLine = old_file_contents[targetAttackIdx + 1]
        if statusLine.startswith("status") and statusLine.endswith("dead") and attackedEntityId in statusLine.split("-"):
            new_file_contents.append(line)
            new_file_contents.append(old_file_contents[lastAttackIdx + 1])
            return lastAttackIdx - lineIdx + 1

    # Attack was NOT conducted until completion. Loop backwards over new_file_contents and delete immediate prior actions on the attacked entity.
    startDeleteIdx = len(new_file_contents) - 1
    for i in range(len(new_file_contents) - 1, -1, -1):
        lineToCheck = new_file_contents[i]
        strings = lineToCheck.split("-")

        # If we hit an action that DOES NOT refer to this entity, we went too far
        if lineToCheck.startswith("!") and attackedEntityId not in strings:
            break

        # If we hit an action that DOES refer to this attacked entity, move the starting delete index to right after the next previous empty string
        if lineToCheck.startswith("!") and attackedEntityId in strings:
            prevLine = lineToCheck
            while prevLine != "":
                prevLine = new_file_contents[i - 1]
                startDeleteIdx = i
                i -= 1

    # Delete everything that referenced this entity that was attacked but never killed in a row
    del new_file_contents[startDeleteIdx:len(new_file_contents)]
    return lastAttackIdx - lineIdx + 1


def processLogFile(filePath):
    """
    Given a full, absolute path to a log file, parse the file and fix any issues, rewriting the result back out to the file.
    """
    global id_counters, old_file_contents, new_file_contents, id_map, dead_entities, didPassEndMarker

    # Reset the global variables at the start of a new log
    resetGlobals()

    with open(filePath, "r") as logFile:
        line = logFile.readline()
        while line:
            nextLine = logFile.readline()
            if not nextLine:
                old_file_contents.append(line)
            else:
                old_file_contents.append(line[:-1]) # Do not include newline at the end of each line
            line = nextLine

    lineIdx = -1
    while lineIdx < len(old_file_contents) - 1:
        lineIdx += 1
        line = old_file_contents[lineIdx]
        shouldAddLine = True

        # ============================================================
        # Whole Line Checks
        # ============================================================
        # Empty string
        if line == "":
            shouldAddLine = handleEmptyLine(line)
        # ClosestXXX declaration
        elif line.startswith("closest"):
            shouldAddLine = handleClosestXXXLine(line)
        # Entering final state output
        elif line.startswith("END"):
            didPassEndMarker = True
        # Defining a new entity
        elif line.startswith("agents") or line.startswith("mobs") or line.startswith("items"):
            line = handleEntityDefinitionLine(line)
        # Attacking an entity
        elif line.startswith("!ATTACK"):
            lineIdx += handleAttackLine(line, lineIdx)
            continue    # Handling for attack alters the new_final_contents... we should immediately move to next line


        # ============================================================
        # Split Line Checks
        # ============================================================
        if shouldAddLine:
            strings = line.split("-")
            for idx in range(0, len(strings)):
                # Found an entity id - map it to the simpler version
                if strings[idx] in id_map:
                    strings[idx] = id_map[strings[idx]]

                # Found an entity referenced after dying
                if not didPassEndMarker and strings[idx] in dead_entities:
                    shouldAddLine = False
                    break
            line = "-".join(strings)  # Rejoin

        # ============================================================
        # More Whole Line Checks (after mapping IDs)
        # ============================================================
        # Declaring an entity as either alive or dead
        if line.startswith("status"):
            shouldAddLine = handleEntityStatusLine(line)

        if shouldAddLine:
            new_file_contents.append(line)

    # Output the list of strings back to the file with the same name
    with open(filePath, "w+") as newFile:
        newFile.write("\n".join(new_file_contents))

def main():
    """
    Main method.
    """
    global WORKING_DIR
    WORKING_DIR = os.getcwd()

    if not doesLogDirectoryExist():
        print("Error - Output directory '{}' does not exist.".format(os.path.join(WORKING_DIR, "logs")))

    logFilePaths = getLogFilePaths()
    for path in logFilePaths:
        processLogFile(path)

if __name__ == "__main__":
    main()