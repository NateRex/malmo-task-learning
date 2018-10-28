# ==============================================================================================
# This file exposes functionality for logging traces containing both state and action
# information of a particular agent at regular intervals.
# ==============================================================================================
from datetime import datetime
import os
import time
from Constants import *
from Utils import *

class Logger:
    """
    Purely static class containing functionality for logging traces containing state and action information
    as a result of actions performed by a companion agent. All of the methods in this class should be called
    from a corresponding action method, such that the trace output is produced as a direct result of performing
    an action.
    """
    __contents = ""                 # The string containing the entire log
    __declaredEntityIds = []        # A list of entity ids for entities that have already been declared in the log

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
    def __areActionsEqual__(actionA, actionB):
        """
        Internal method for determining whether two actions are equivalent.
        """
        if actionA.type != actionB.type:
            return False
        if len(actionA.args) != len(actionB.args):
            return False
        for i in range(0, len(actionA.args)):
            if type(actionA.args[i]) != type(actionB.args[i]) or actionA.args[i] != actionB.args[i]:
                return False
        return True

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

    __lastClosestEntity = None

    @staticmethod
    def logClosestEntity(agent, entity):
        """
        Log the closest entity to the agent given.
        """
        agentId = agent.getId()
        if agentId == None:
            return

        if Logger.__lastClosestEntity == None or entity.id != Logger.__lastClosestEntity.id:
            Logger.__pushStatement__("closest_entity-{}-{}-{}".format(agentId, entity.type, entity.id))
            Logger.__lastClosestEntity = entity

    __lastMoveTo = None             # Keep track of the last moveTo executed to avoid repeat logging
    __lastMoveToDidFinish = False   # Keep track of whether or not moveTo has finished to log post-conditions

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
        command = Action("moveto", [agentId, entity.id])
        if Logger.__lastMoveTo != None and Logger.__areActionsEqual__(Logger.__lastMoveTo, command):
            return

        # This might be an entity not previously declared in the log. Log it if so.
        Logger.__logNewEntity__(entity)

        # Pre-conditions
        if agent.lastMovedTo != None:
            Logger.__pushStatement__("agent_at-{}-{}".format(agentId, agent.lastMovedTo))

        # Action
        Logger.__pushStatement__("!MOVETO-{}-{}".format(agentId, entity.id))
        Logger.__lastMoveTo = command

    @staticmethod
    def logMoveToFinish(agent, entity):
        """
        Log the postconditions for the MoveTo command, since it has ran to completion before executing another command.
        """
        agentId = agent.getId()
        if agentId == None:
            return

        # Command already ran to completion
        if Logger.__lastMoveToDidFinish:
            return

        Logger.__pushStatement__("agent_at-{}-{}".format(agentId, entity.id))
        Logger.__lastMoveToDidFinish = True


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
