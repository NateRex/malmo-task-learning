# ==============================================================================================
# This file exposes functionality for logging traces containing both state and action
# information of a particular agent at regular intervals.
# ==============================================================================================
from datetime import datetime
import os
import time
from Constants import *

class Logger:
    """
    Purely static class containing functionality for logging traces containing state and action information
    as a result of actions performed by a companion agent. All of the methods in this class should be called
    from a corresponding action method, such that the trace output is produced as a direct result of performing
    an action.
    """
    __contents = ""
    __declaredEntityIds = []        # A list of entity ids for entities that have already been declared in the log
    __lastCommand = None            # A possible action that was started but has not yet finished
    __lastCommandFinished = False   # Indicates whether the last command finished to completion

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
    def __commandAlreadyStarted__(command):
        """
        Internal method that returns true if the given command is a repeat of the last command that was started and has not yet finished.
        Returns false otherwise.
        """
        if Logger.__lastCommand == None:
            return False
        if len(command) != len(Logger.__lastCommand):
            return False
        for i in range(0, len(command)):
            if type(command[i]) != type(Logger.__lastCommand[i]) or command[i] != Logger.__lastCommand[i]:
                return False
        return True 

    @staticmethod
    def __markCommandStarted__(command):
        """
        Internal method that marks a new command as having been started.
        """
        Logger.__lastCommand = command
        Logger.__lastCommandFinished = False

    @staticmethod
    def __markCommandFinished__():
        """
        Internal method that marks the last ran command as having finished.
        """
        Logger.__lastCommandFinished = True

    @staticmethod
    def __logNewEntity__(entity):
        """
        Internal method that logs the definition of a new entity, and adds its id to the list of declared entities.
        """
        if entity.id in Logger.__declaredEntityIds:  # We already logged this entity
            return

        if entity.type not in MobType.__members__:  # Is an agent
            Logger.__pushStatement__("entities-{}-agent".format(entity.id))
        else:   # Is a mob
            Logger.__pushStatement__("entities-{}-{}".format(entity.id, entity.type))
        Logger.__declaredEntityIds.append(entity.id)

    @staticmethod
    def logInitialState(agents):
        """
        Given the list of agents for a mission, log the starting state for the environment in the log.
        """
        # Define all starting entities
        for agent in agents:
            entities = agent.getNearbyEntities()
            if entities == None:
                return
            for entity in entities:
                Logger.__logNewEntity__(entity)

        Logger.__pushStatement__("START\n")

    @staticmethod
    def logFinalState():
        """
        Log the end state for the environment in the log.
        """
        Logger.__pushStatement__("\nEND")
        # TODO

    @staticmethod
    def logMoveToStart(agent, entity):
        """
        Log the preconditions and action identifier for the MoveTo command, provided that it is unique
        from the previous action.
        """
        agentId = agent.getId()
        if agentId == None:
            return

        # Ensure this is not a repeat call to do what we were already doing
        command = ("moveto", agentId, entity.id)
        if Logger.__commandAlreadyStarted__(command):
            return

        # This might be an entity not previously declared in the log. Log it if so.
        Logger.__logNewEntity__(entity)

        # Pre-conditions
        if agent.lastMovedTo != None:
            Logger.__pushStatement__("agent_at-{}-{}".format(agentId, agent.lastMovedTo))

        # Action
        Logger.__pushStatement__("!MOVETO-{}-{}".format(agentId, entity.id))
        Logger.__markCommandStarted__(command)

    @staticmethod
    def logMoveToFinish(agent, entity):
        """
        Log the postconditions for the MoveTo command, since it has ran to completion before executing another command.
        """
        agentId = agent.getId()
        if agentId == None:
            return

        # Command already ran to completion
        if Logger.__lastCommandFinished:
            return

        Logger.__pushStatement__("agent_at-{}-{}".format(agentId, entity.id))
        Logger.__markCommandFinished__()


    @staticmethod
    def logCraft(agent, command):
        """
        Log the preconditions and action identifier for the Craft command, provided that it is unique
        from the previous action.
        """
        if Logger.__commandAlreadyStarted__(command):
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
        fileName = datetime.fromtimestamp(time.time()).strftime('%m_%d_%Y_%H_%M_%S') + ".log"
        filePath = "logs"
        if not os.path.isdir(filePath):
            os.mkdir(filePath)
        filePath = os.path.join(filePath, fileName)
        logFile = open(filePath, "w+")
        logFile.write(Logger.__contents)
        logFile.close()
        print("Mission log output has been saved to: " + filePath)
        Logger.clear()
