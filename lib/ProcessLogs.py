# ==============================================================================================
# This file represents a standalone script for the post-processing of log files. For each file
# in the logs/ directory, parse the log and resolve any minor issues that have resulted due to
# tolerance issues while the mission ran.
# ==============================================================================================
import os

WORKING_DIR = None

def logDirectoryExists():
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
    for (dirpath, dirnames, filenames) in os.walk(logDirPath):
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

            # Checks for each entity, which are separated by '-' in the line ====================
            if shouldAddLine:
                lineParts = line.split("-")
                for part in lineParts:
                    if checkIsMobDead(newFileContents, part):   # No reference to mob after it has died
                        shouldAddLine = False
                        break
            
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

    if not logDirectoryExists():
        print("Error - Output directory '{}' does not exist.".format(os.path.join(WORKING_DIR, "logs")))

    logFilePaths = getLogFilePaths()
    for path in logFilePaths:
        processLogFile(path)

if __name__ == "__main__":
    main()