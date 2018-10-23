# ==============================================================================================
# This file exposes functionality for logging traces containing both state and action
# information of a particular agent at regular intervals.
# ==============================================================================================
from datetime import datetime
import os
import time

class Logger:
    """
    Purely static class containing functionality for logging traces containing state and action information
    as a result of actions performed by a companion agent. All of the methods in this class should be called
    from a corresponding action method, such that the trace output is produced as a direct result of performing
    an action.
    """
    __contents = ""
    __startedCommand = None     # A continuous action that was started but was not yet finished to completion

    @staticmethod
    def clear():
        """
        Clear the contents of this log.
        """
        Logger.__contents = ""

    @staticmethod
    def __getTime__():
        """
        Internal method for getting a string containing the current time and date.
        """
        return datetime.fromtimestamp(time.time()).strftime('%m-%d-%Y %H:%M:%S.%f')

    @staticmethod
    def __pushStatement__(value):
        """
        Internal method for pushing a new statement onto the trace log.
        """
        Logger.__contents += value + "\n"

    @staticmethod
    def __sameAsStartedCommand__(command):
        """
        Returns true if the given command is a repeat of the last command that was started and has not yet finished.
        Returns false otherwise.
        """
        if Logger.__startedCommand == None:
            return False
        if command.type != Logger.__startedCommand.type:
            return False
        if len(command.args) != len(Logger.__startedCommand.args):
            return False
        for i in range(0, len(command.args)):
            if type(command.args[i]) != type(Logger.__startedCommand.args[i]) or command.args[i] != Logger.__startedCommand.args[i]:
                return False
        return True 

    @staticmethod
    def __logMoveToPreconditions__(agent, command):
        # TODO: Log where agent is using some other entity or block
        # TODO: Log where thing we are moving to is at
        return

    @staticmethod
    def __logMoveToPostconditions__(agent, command):
        # TODO: Log where agent is now as a result of moving using some identifier
        return

    @staticmethod
    def logMoveToStart(agent, command):
        """
        Log the preconditions and action identifier for the MoveTo command, provided that it is unique
        from the previous action.
        """
        if Logger.__sameAsStartedCommand__(command):
            return
        # TODO: If Logger.__currentCommand != None... do some wrap up of old command
        agentPos = agent.getPosition()
        if agentPos == None:
            return
        Logger.__logMoveToPreconditions__(agent, command)
        Logger.__pushStatement__("!MOVETO-{}-({},{},{})-({},{},{})".format("PLACEHOLDER", command.args.start.x, command.args.start.y, command.args.start.z, command.args.finish.x, command.args.finish.y, command.args.finish.z,))

    @staticmethod
    def logMoveToFinish(agent, command):
        """
        Log the postconditions for the MoveTo command, since it has ran to completion before executing another command.
        """
        if not Logger.__sameAsStartedCommand__(command):    # We started another command before finishing this one
            return
        Logger.__logMoveToPostconditions__(agent, command)
        Logger.__startedCommand = None

    @staticmethod
    def logCraft(agent, command):
        """
        Log the preconditions and action identifier for the Craft command, provided that it is unique
        from the previous action.
        """
        if Logger.__sameAsStartedCommand__(command):
            return
        # TODO: If Logger.__currentCommand != None... do some wrap up of old command
        for recipeItem in command.args.recipe:
            Logger.__pushStatement__("agent_has-{}-{}".format("PLACEHOLDER", recipeItem.value))
        Logger.__pushStatement__("!CRAFT-{}-{}".format("PLACEHOLDER", command.item.value))
        for recipeItem in command.args.recipe:
            if agent.amountOfItemInInventory(recipeItem) <= 0:
                Logger.__pushStatement__("agent_not_have-{}-{}".format("PLACEHOLDER", recipeItem.value))
        Logger.__pushStatement__("agent_has-{}-{}".format("PLACEHOLDER", command.item.value))

    @staticmethod
    def flushToFile():
        """
        Outputs the current JSON log string to a file located a the 'logs' directory within the current working
        directory. The file name is determined by the current date and time.
        """
        if len(Logger.__contents) > 1:
            Logger.__contents = Logger.__contents[:-1]
        Logger.__contents += "]"
        fileName = datetime.fromtimestamp(time.time()).strftime('%m_%d_%Y_%H_%M_%S') + "_log.json"
        filePath = "logs"
        if not os.path.isdir(filePath):
            os.mkdir(filePath)
        filePath = os.path.join(filePath, fileName)
        logFile = open(filePath, "w+")
        logFile.write(Logger.__contents)
        logFile.close()
        print("Mission log output has been saved to: " + filePath)
        Logger.clear()
