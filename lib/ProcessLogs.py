# ==============================================================================================
# This file represents a standalone script for the post-processing of log files. For each file
# in the logs/ directory, parse the log and resolve any minor issues that have resulted due to
# tolerance issues while the mission ran.
# ==============================================================================================
import os

WORKING_DIR = None  # Current working directory of this script

def getNextIdNumberForType(id_counters, entityType):
    """
    Returns the next ID number for use for a specific type of entity.
    """
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
            filepath = os.path.join(dirpath, filename)
            paths.append(filepath)
    return paths

def checkIsMobDead(fileContents, mobId):
    """
    Given a portion of a log file's contents as an array of strings, check to see if a mob of the given id was already declared dead.
    """
    toCheckStr = "is_dead-{}".format(mobId)
    for line in fileContents:
        if line == toCheckStr:
            return True
    return False

def processLogFile(filePath):
    """
    Given a full, absolute path to a log file, parse the file and fix any issues, rewriting the result back out to the file.
    """
    id_counters = {}    # A global counter for each type of entity to map complex Malmo ids to simpler ones
    id_map = {}         # Dictionary to map ids of certain types to new ids to simplify them

    # Generate a list of strings representing the lines of the NEW file post-processing
    newFileContents = []
    with open(filePath, "r") as logFile:
        line = logFile.readline()
        while line:
            shouldAddLine = True

            # Checks for the entire line ===================
            if line == "\n" and len(newFileContents) > 0 and newFileContents[-1] == "\n":   # No repeated newlines
                shouldAddLine = False
            elif line == "\n" and len(newFileContents) > 0 and newFileContents[-1].startswith("closest"):   # No newline after closest entity output
                shouldAddLine = False
            elif line.startswith("closest") and len(newFileContents) > 0 and newFileContents[-1].startswith("!"):   # Need newline after last action that didn't finish
                newFileContents.append("\n")

            # Checks for each part in the line, separated by '-' ===================
            if shouldAddLine:
                if line.startswith("agents") or line.startswith("mobs") or line.startswith("items"): # Simplify ids of entities during definition
                    # Simplify ids of entities during definition
                    lineParts = line.split("-")
                    oldId = lineParts[1]
                    entityType = lineParts[2][:-1]  # Don't include newline at end of entity type
                    if oldId in id_map:
                        lineParts[1] = id_map[oldId]
                    else:
                        newId = "{}{}".format(entityType, getNextIdNumberForType(id_counters, entityType))
                        id_map[oldId] = newId
                        id_map[newId] = newId
                        lineParts[1] = newId
                    line = "-".join(lineParts)

                lineParts = line.split("-")
                for partIdx in range(0, len(lineParts)):
                    # Replace entity id with simpler one if currently processing an id (consider that last character could be newline)
                    if lineParts[partIdx] in id_map:
                        lineParts[partIdx] = id_map[lineParts[partIdx]]
                    elif lineParts[partIdx][:-1] in id_map:
                        lineParts[partIdx] = id_map[lineParts[partIdx][:-1]]
                        lineParts[partIdx] += "\n"

                    # Check if a mob or agent is referenced after dying
                    if checkIsMobDead(newFileContents, lineParts[partIdx]):
                        shouldAddLine = False
                        break
                line = "-".join(lineParts)

            if shouldAddLine:
                newFileContents.append(line)
            line = logFile.readline()

    # Output the list of strings back to the file with the same name
    with open(filePath, "w+") as newFile:
        newFile.write("".join(newFileContents))

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