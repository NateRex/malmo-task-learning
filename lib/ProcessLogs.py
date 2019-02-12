#!/usr/bin/python
# ==============================================================================================
# This file represents a standalone script for the post-processing of log files. For each file
# in the logs/ directory, parse the log and resolve any minor issues that have resulted due to
# tolerance issues while the mission ran.
# ==============================================================================================
import os
import sys

# GLOBALS FOR ALL LOGS
WORKING_DIR = None          # Current working directory of this script
TOTAL_LOGS = 0              # Total number of logs processed
LOGS_DELETED = 0            # Number of logs that were deleted due to unmet conditions specified by parameters
MIN_KILLS = 0               # Minimum number of kills that must be made by the agents in order to preserve log
MIN_LINES = 0               # Minimum number of lines that the new log must have in order to preserve it
ACTION_POST_TUPLES = {      # A set of tuples to show what post-condition is expected immediately following an action
    "!LOOKAT" : "agent_looking_at",
    "!MOVETO" : "agent_at",
    "!ATTACK" : "status"
}

# GLOBALS FOR EACH LOG
old_file_contents = []      # A list of the lines for the original log file
new_file_contents = []      # A list of the lines for the new log file after post-processing
id_counters = {}            # A global counter for each type of entity for generating new simple entity ids
id_map = {}                 # A mapping of original complex Malmo ids to simpler ones generated in this script
dead_entities = []          # A list of ids for entities that have been declared as dead
startMarkerIndex = None     # Location in the log of the START marker
endMarkerIndex = None       # Location in the log of the END marker


def resetGlobals():
    """
    Reset the global values so that they are ready to be used for processing a new log.
    """
    global id_counters, old_file_contents, new_file_contents, id_map, dead_entities, startMarkerIndex, endMarkerIndex
    old_file_contents = []
    new_file_contents = []
    id_counters = {}
    id_map = {}
    dead_entities = []
    startMarkerIndex = None
    endMarkerIndex = None

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

def getLine(idx):
    """
    Get a line from the original log file by index, making any necessary adjustments to it before returning it.
    """
    line = old_file_contents[idx]
    strings = line.split("-")
    for idx in range(0, len(strings)):
        # Replace old entity ids with new ones if they were previously generated
        if strings[idx] in id_map:
            strings[idx] = id_map[strings[idx]]
    return "-".join(strings)

def addLine(line):
    """
    Before appending a new line to the output list of strings for a log, perform additional checks on each part of the line, separated by '-'.
    """
    strings = line.split("-")
    for idx in range(0, len(strings)):
        # If an entity is referenced after already dying, do not add the line
        if endMarkerIndex == None and strings[idx] in dead_entities:
            # Some actions reference a dead entity as the thing we are "looking FROM", "moving FROM", etc...
            if line.startswith("!") and idx == 2 and len(strings) > 3:
                continue
            return
    new_file_contents.append("-".join(strings))

# ======================================================================
# Operations on original log
# ======================================================================

def handleEmptyLine(line):
    """
    Handle the case when a line contains the empty string "".
    """
    global new_file_contents
    if len(new_file_contents) > 0:
        if new_file_contents[-1] == "": # No repeated newlines
            return
        if new_file_contents[-1].startswith("closest"): # No newline after closest_XXX entity output
            return
    addLine(line)

def handleClosestXXXLine(line):
    """
    Handle the case where the line is defining a closest entity to one of the agents.
    """
    global new_file_contents
    if len(new_file_contents) > 0 and new_file_contents[-1].startswith("!"):    # Last action never finished... add a newline before proceeding
        addLine("")
    addLine(line)

def handleEntityDefinitionLine(line):
    """
    Handle the case where the line is defining a new entity.
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
    addLine("-".join(strings))
    
def handleEntityStatusLine(line):
    """
    Handle the case where the line is declaring an entity as either alive or dead.
    """
    global dead_entities
    addLine(line)
    if line.endswith("dead") and endMarkerIndex == None:
        strings = line.split("-")
        dead_entities.append(strings[1])

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
        lineToCheck = getLine(i)
        if not lineToCheck.startswith("!"):
            continue
        else:
            if lineToCheck.startswith("!ATTACK") and lineToCheck.endswith(attackedEntityId):
                lastAttackIdx = i
                nextLine = getLine(i + 1) if i < len(old_file_contents) - 1 else ""
                if nextLine.startswith("status"):
                    targetAttackIdx = i
            else:
                break

    # If this attack ended with the entity dying, make sure it is officially logged and return to move ahead in the log past the status update
    if targetAttackIdx != None:
        statusLine = getLine(targetAttackIdx + 1)
        if statusLine.startswith("status") and statusLine.endswith("dead") and attackedEntityId in statusLine.split("-"):
            new_file_contents.append(line)
            handleEntityStatusLine(getLine(targetAttackIdx + 1))
            return lastAttackIdx - lineIdx if lastAttackIdx != targetAttackIdx else lastAttackIdx - lineIdx + 1

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
    return lastAttackIdx - lineIdx

# ======================================================================
# Operations on newly generated log
# ======================================================================

def checkActionPreconditions(idx, checkClosest=False):
    """
    Given a line index of an action in the newly generated log contents, make sure that each pre-condition has been set beforehand in the log.
    Returns 0 if no changes occurred, > 0 for the amount the log was truncated by (if any), and -1 if the log should be discarded.
    """
    global new_file_contents
    # Gather all of the preconditions we will be checking for
    startIdx = idx
    preconditions = []
    preconditionLineNumbers = []
    for i in range(idx - 1, -1, -1):
        startIdx = i
        # Newline is the stopping point
        if new_file_contents[i] == "":
            break
        # ClosestXXX comes in at random (ignore)
        elif new_file_contents[i].startswith("closest"):
            if checkClosest == True:
                preconditions.append(new_file_contents[i].split("-"))
                preconditionLineNumbers.append(i)
            else:
                continue
        # Add the precondition
        else:
            preconditions.append(new_file_contents[i].split("-"))
            preconditionLineNumbers.append(i)

    # Loop backwards and check for the postconditions having been set. Note: if a precondition is set with the wrong values, then it is still a failure
    linesDeleted = 0
    for i in range(startIdx, -1, -1):
        lineToCheck = new_file_contents[i].split("-")
        for j in range(0, len(preconditions)):
            if lineToCheck[0] == preconditions[j][0] and lineToCheck[1] == preconditions[j][1]:     # If 1st two args match, ensure the entire lines match
                if len(lineToCheck) != len(preconditions[j]):
                    return -1
                allValuesMatch = True
                for k in range(0, len(preconditions[j])):
                    if lineToCheck[k] != preconditions[j][k]:
                        allValuesMatch = False

                # ClosestXXX is a special case, where if we are checking preconditions for the FIRST action, it must appear in initial state
                if preconditions[j][0].startswith("closest") and checkClosest == True:
                    if not allValuesMatch:  # Modify closestXXX in initial state to match
                        new_file_contents[i] = "-".join(preconditions[j])
                    
                    # Remove closestXXX before action
                    del new_file_contents[preconditionLineNumbers[j]]
                    linesDeleted += 1
                    allValuesMatch = True

                if not allValuesMatch:
                    return -1
                del preconditions[j]
                break

    # If not all preconditions were set, return false
    if len(preconditions) > 0:
        return -1
    else:
        return linesDeleted

def checkActionPostconditions(idx):
    """
    Given a line index of an action in the newly generated log contents, make sure the action is followed by its expected post-conditions.
    Returns the new length of new_file_contents.
    """
    global new_file_contents

    line = new_file_contents[idx]
    action = line.split("-")[0]

    # Received a line that was not an expected action
    if action not in ACTION_POST_TUPLES:
        return 0

    # Action was followed by its expected immediate post-condition
    if idx + 1 < len(new_file_contents) and new_file_contents[idx + 1].startswith(ACTION_POST_TUPLES[action]):
        return 0

    # Action was not followed by its expected immedate post-condition. Delete from the previous newline to the next newline.
    startDeleteIdx = idx
    for i in range(idx, -1, -1):
        startDeleteIdx = i
        if new_file_contents[i] == "":
            break
    endDeleteIdx = idx
    for i in range(idx, len(new_file_contents)):
        endDeleteIdx = i
        if new_file_contents[i] == "":
            break
    orignalLength = len(new_file_contents)
    del new_file_contents[startDeleteIdx:endDeleteIdx]
    return orignalLength - len(new_file_contents)

def fixActionFromParameter(idx):
    """
    Given the line index of an action in the newly generated log contents, ensure that the parameter denoting where we last acted on is correct,
    after having potentially deleted previous parts of the original log.
    """
    global new_file_contents

    line = new_file_contents[idx]
    strings = line.split("-")
    statePrefix = None
    entity = None
    expectedParam = None
    if line.startswith("!LOOKAT"):
        statePrefix = "agent_looking_at"
        entity = strings[1]
        expectedParam = strings[2]
    elif line.startswith("!MOVETO"):
        statePrefix = "agent_at"
        entity = strings[1]
        expectedParam = strings[2]
    else:
        return  # Only applies to certain actions

    # Loop upwards through the new log for the first appearance of the statePrefix, and ensure that the parameter in the action matches
    for i in range(idx, -1, -1):
        stringsToCheck = new_file_contents[i].split("-")
        if stringsToCheck[0].startswith(statePrefix) and stringsToCheck[1] == entity:
            actualParam = stringsToCheck[2]
            if actualParam != expectedParam:
                strings[2] = actualParam
                new_file_contents[idx] = "-".join(strings)
            return

def processLogFile(filePath):
    """
    Given a full, absolute path to a log file, parse the file and fix any issues, rewriting the result back out to the file.
    """
    global LOGS_DELETED, id_counters, old_file_contents, new_file_contents, id_map, dead_entities, startMarkerIndex, endMarkerIndex

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

    # ============================================================
    # Copy old log -> new log, applying adjustments
    # ============================================================
    lineIdx = -1
    while lineIdx < len(old_file_contents) - 1:
        lineIdx += 1
        line = getLine(lineIdx)
        shouldAddLine = True

        # ============================================================
        # Line Checks
        # ============================================================
        # Empty string
        if line == "":
            handleEmptyLine(line)
            continue
        # ClosestXXX declaration
        elif line.startswith("closest"):
            handleClosestXXXLine(line)
            continue
        # Leaving initial state output
        elif line.startswith("START"):
            startMarkerIndex = lineIdx
            addLine(line)
            continue
        # Entering final state output
        elif line.startswith("END"):
            endMarkerIndex = lineIdx
            addLine(line)
            continue
        # Defining a new entity
        elif line.startswith("agents") or line.startswith("mobs") or line.startswith("items"):
            handleEntityDefinitionLine(line)
            continue
        # Declaring an entity as either alive or dead
        elif line.startswith("status"):
            handleEntityStatusLine(line)
            continue
        # Attacking an entity
        elif line.startswith("!ATTACK"):
            lineIdx += handleAttackLine(line, lineIdx)
            continue
        # Default case... just add the line
        else:
            addLine(line)
            continue

    # ============================================================
    # Perform additional cleanup on new log
    # ============================================================
    lineIdx = -1
    new_file_len = len(new_file_contents)
    startMarkerIndex = None
    endMarkerIndex = None
    nextActionIsFirstAction = True
    while lineIdx < new_file_len - 1:
        lineIdx += 1
        line = new_file_contents[lineIdx]
        strings = line.split("-")

        # ============================================================
        # Line Checks
        # ============================================================
        # Leaving initial state output
        if line.startswith("START"):
            startMarkerIndex = lineIdx
            continue
        # If line represents an action
        elif strings[0] in ACTION_POST_TUPLES:
            # If it is a LOOKAT or MOVETO command, possibly fix the 3rd parameter of where we looked/moved from previously after deleting parts of the log
            fixActionFromParameter(lineIdx)

            # Check that each action's preconditions were actually set before-hand
            if nextActionIsFirstAction and startMarkerIndex != None:
                nextActionIsFirstAction = False
                returnValue = checkActionPreconditions(lineIdx, True)   # First action means 
            else:
                returnValue = checkActionPreconditions(lineIdx)
            if returnValue < 0:
                os.remove(filePath)
                LOGS_DELETED += 1
                return
            elif returnValue > 0:   # Just in case, move back that number of lines and continue
                lineIdx -= (returnValue + 1)
                new_file_len -= returnValue
                continue
    
            # Check that each action is followed by its expected post-conditions
            returnValue = checkActionPostconditions(lineIdx)
            if returnValue > 0:    # Just in case, move back that number of lines and continue
                lineIdx -= (returnValue + 1)
                new_file_len -= returnValue
                continue
            continue

    # Output the list of strings back to the file with the same name
    with open(filePath, "w+") as newFile:
        newFile.write("\n".join(new_file_contents))

    # Do any additional parameter checks to see if we should keep the file
    if len(dead_entities) < MIN_KILLS:
        os.remove(filePath)
        LOGS_DELETED += 1
    if len(new_file_contents) < MIN_LINES:
        os.remove(filePath)
        LOGS_DELETED += 1

def main():
    """
    Main method.
    """
    global WORKING_DIR, TOTAL_LOGS, MIN_KILLS, MIN_LINES

    # Process command-line parameters
    if "-h" in sys.argv:
        print("Usage: {} <args>".format(sys.argv[0]))
        print("-h : Display this help message")
        print("-l <amt> : New log must contain <amt> number of lines (delete log otherwise)")
        print("-k <amt> : Companion must kill <amt> number of entities (delete log otherwise)")
        return
    if "-k" in sys.argv:
        kIndex = sys.argv.index("-k")
        if kIndex == len(sys.argv) - 1:
            print("Error - No amount specified for argument '-k'")
            return
        try:
            MIN_KILLS = int(sys.argv[kIndex + 1])
        except ValueError:
            print("Error - '{}' is not a valid input for argument '{}'".format(sys.argv[kIndex + 1], sys.argv[kIndex]))
            return
    if "-l" in sys.argv:
        lIndex = sys.argv.index("-l")
        if lIndex == len(sys.argv) - 1:
            print("Error - No amount specified for argument '-l'")
            return
        try:
            MIN_LINES = int(sys.argv[lIndex + 1])
        except ValueError:
            print("Error - '{}' is not a valid input for argument '{}'".format(sys.argv[lIndex + 1], sys.argv[lIndex]))
            return

    WORKING_DIR = os.getcwd()
    if not doesLogDirectoryExist():
        print("Error - Output directory '{}' does not exist.".format(os.path.join(WORKING_DIR, "logs")))

    logFilePaths = getLogFilePaths()
    TOTAL_LOGS = len(logFilePaths)
    for path in logFilePaths:
        processLogFile(path)

    print("Logs cleaned: {}".format(TOTAL_LOGS - LOGS_DELETED))
    print("Logs deleted: {}".format(LOGS_DELETED))

if __name__ == "__main__":
    main()