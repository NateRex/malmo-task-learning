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
    def __logAgent__(agent):
        """
        Internal method that logs the definition of a new agentm and adds its id information to the list of declared entities.
        """
        agentId = agent.getId()
        if agentId == None:
            return
        if agentId in Logger.__declaredEntityIds:   # We already logged this agent
            return

        Logger.__pushStatement__("agent-{}".format(agentId))
        Logger.__declaredEntityIds.append(agentId)

    @staticmethod
    def __logEntity__(entity):
        """
        Internal method that logs the definition of a new entity, and adds its id to the list of declared entities.
        """
        if entity.id in Logger.__declaredEntityIds:  # We already logged this entity
            return

        if entity.type in MobType.Hostile.__members__ or entity.type in MobType.Peaceful.__members__:  # Avoid redeclaring agents as entities
            Logger.__pushStatement__("entities-{}-{}".format(entity.type, entity.id))
            Logger.__declaredEntityIds.append(entity.id)

    @staticmethod
    def __logAgentInventory__(agent):
        """
        Internal method that logs everything that an agent has in their inventory.
        """
        agentId = agent.getId()
        inventory = agent.getInventoryJson()
        if agentId == None or inventory == None:
            return

        for i in range(0, len(inventory)):
            Logger.__pushStatement__("agent_has-{}-{}".format(agentId, inventory[i]["type"]))

    @staticmethod
    def logInitialState(agents):
        """
        Given the list of agents for a mission, log the starting state for the environment in the log.
        """
        for agent in agents:
            entities = agent.getNearbyEntities()
            if entities == None:
                return

            # Define all starting nearby entities to this agent
            for entity in entities:
                Logger.__logEntity__(entity)

            # Log out this agent's starting inventory
            Logger.__logAgentInventory__(agent)

        Logger.__pushStatement__("START\n")

    @staticmethod
    def logFinalState():
        """
        Log the end state for the environment in the log.
        """
        Logger.__pushStatement__("END")
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

        # This might be an entity not previously declared in the log. Log it if so.
        Logger.__logEntity__(entity)

        if Logger.__lastClosestEntity == None or entity.id != Logger.__lastClosestEntity.id:
            Logger.__pushStatement__("closest_entity-{}-{}-{}".format(agentId, entity.type, entity.id))
            Logger.__lastClosestEntity = entity

    __lastClosestEntitiesByType = []    # Stores an array of the last closest entity logged for each type

    @staticmethod
    def logClosestEntityByType(agent, entity):
        """
        Log the closest entity of a specific type to the agent given.
        """
        agentId = agent.getId()
        if agentId == None:
            return

        # This might be an entity not previously declared in the log. Log it if so.
        Logger.__logEntity__(entity)

        for i in range(0, len(Logger.__lastClosestEntitiesByType)):
            if entity.type == Logger.__lastClosestEntitiesByType[i].type:
                if entity.id != Logger.__lastClosestEntitiesByType[i].id:   # Previously logged of this entity type and they differ
                    Logger.__pushStatement__("closest_{}-{}-{}".format(entity.type, agentId, entity.id))
                    Logger.__lastClosestEntitiesByType[i] = entity
                else:   # Previously logged of this entity type and the entity is the same
                    return

        Logger.__pushStatement__("closest_{}-{}-{}".format(entity.type, agentId, entity.id))
        Logger.__lastClosestEntitiesByType.append(entity)    

    __lastClosestPeacefulEntity = None

    @staticmethod
    def logClosestPeacefulEntity(agent, entity):
        """
        Log the closest peaceful entity to the agent given.
        """
        agentId = agent.getId()
        if agentId == None:
            return

        # This might be an entity not previously declared in the log. Log it if so.
        Logger.__logEntity__(entity)

        if Logger.__lastClosestPeacefulEntity == None or entity.id != Logger.__lastClosestPeacefulEntity.id:
            Logger.__pushStatement__("closest_peaceful_entity-{}-{}-{}".format(agentId, entity.type, entity.id))
            Logger.__lastClosestPeacefulEntity = entity

    __lastClosestHarmfulEntity = None

    @staticmethod
    def logClosestHarmfulEntity(agent, entity):
        """
        Log the closest harmful entity to the agent given.
        """
        agentId = agent.getId()
        if agentId == None:
            return

        # This might be an entity not previously declared in the log. Log it if so.
        Logger.__logEntity__(entity)

        if Logger.__lastClosestHarmfulEntity == None or entity.id != Logger.__lastClosestHarmfulEntity.id:
            Logger.__pushStatement__("closest_harmful_entity-{}-{}-{}".format(agentId, entity.type, entity.id))
            Logger.__lastClosestHarmfulEntity = entity

    __lastLookAt = None             # Keep track of the last lookAt executed to avoid repeat logging
    __lastLookAtDidFinish = False   # Keep track of whether or not lookAt has finished to log post-conditions

    @staticmethod
    def logLookAtStart(agent, entity):
        """
        Log the preconditions and action for the LookAt command, provided that it is not a repeat
        call of the previous LookAt command.
        """
        agentId = agent.getId()
        if agentId == None:
            return

        # Ensure this is not a repeat call to do what we were already doing
        command = Action("lookat", [agentId, entity.id])
        if Logger.__lastLookAt != None and Logger.__areActionsEqual__(Logger.__lastLookAt, command):
            return

        # This might be an entity not previously declared in the log. Log it if so.
        Logger.__logEntity__(entity)

        # Pre-conditions
        if agent.lastLookedAt != None:
            Logger.__pushStatement__("agent_looking_at-{}-{}".format(agentId, agent.lastLookedAt))

        # Action
        Logger.__pushStatement__("!LOOKAT-{}-{}".format(agentId, entity.id))
        Logger.__lastLookAt = command
        Logger.__lastLookAtDidFinish = False

    @staticmethod
    def logLookAtFinish(agent, entity):
        """
        Log the postconditions for the LookAt command, since it has ran to completion before looking elsewhere
        """
        agentId = agent.getId()
        if agentId == None:
            return

        # Did command already run to completion (and was therefore postconditions were logged)?
        if Logger.__lastLookAtDidFinish:
            return

        Logger.__pushStatement__("agent_looking_at-{}-{}".format(agentId, entity.id))
        Logger.__pushStatement__("")    # Add a newline
        Logger.__lastLookAtDidFinish = True

    __lastMoveTo = None             # Keep track of the last moveTo executed to avoid repeat logging
    __lastMoveToDidFinish = False   # Keep track of whether or not moveTo has finished to log post-conditions
    
    @staticmethod
    def logMoveToStart(agent, entity):
        """
        Log the preconditions and action for the MoveTo command, provided that it is not a repeat
        call of the previous LookAt command.
        """
        agentId = agent.getId()
        if agentId == None:
            return

        # Ensure this is not a repeat call to do what we were already doing
        command = Action("moveto", [agentId, entity.id])
        if Logger.__lastMoveTo != None and Logger.__areActionsEqual__(Logger.__lastMoveTo, command):
            return

        # This might be an entity not previously declared in the log. Log it if so.
        Logger.__logEntity__(entity)

        # Pre-conditions
        if agent.lastLookedAt != None:
            Logger.__pushStatement__("agent_looking_at-{}-{}".format(agentId, agent.lastLookedAt))
        if agent.lastMovedTo != None:
            Logger.__pushStatement__("agent_at-{}-{}".format(agentId, agent.lastMovedTo))

        # Action
        Logger.__pushStatement__("!MOVETO-{}-{}".format(agentId, entity.id))
        Logger.__lastMoveTo = command
        Logger.__lastMoveToDidFinish = False

    @staticmethod
    def logMoveToFinish(agent, entity):
        """
        Log the postconditions for the MoveTo command, since it has ran to completion before moving elsewhere.
        """
        agentId = agent.getId()
        if agentId == None:
            return

        # Did command already run to completion (and was therefore postconditions were logged)?
        if Logger.__lastMoveToDidFinish:
            return

        Logger.__pushStatement__("agent_at-{}-{}".format(agentId, entity.id))
        Logger.__pushStatement__("")    # Add newline
        Logger.__lastMoveToDidFinish = True

    @staticmethod
    def logCraft(agent, item, recipeItems):
        """
        Log the preconditions, action, and postconditions for the Craft command.
        """
        agentId = agent.getId()
        if agentId == None:
            return

        # Preconditions
        for recipeItem in recipeItems:
            Logger.__pushStatement__("agent_has-{}-{}".format(agentId, recipeItem.value))

        # Action
        Logger.__pushStatement__("!CRAFT-{}-{}".format(agentId, item.value))

        # Postconditions
        Logger.__pushStatement__("agent_has-{}-{}".format(agentId, item.value))
        for recipeItem in recipeItems:
            if agent.amountOfItemInInventory(recipeItem) <= 0:
                Logger.__pushStatement__("agent_lost-{}-{}".format(agentId, recipeItem.value))
        Logger.__pushStatement__("")    # Add a newline

    __lastAttack = None     # Keep track of the last entity we attacked to avoid unnecessary repeat logs

    @staticmethod
    def logAttack(agent, entity, didKill):
        """
        Log the action and possible postconditions for the Attack command.
        """
        agentId = agent.getId()
        if agentId == None:
            return

        # Preconditions
        Logger.__pushStatement__("agent_looking_at-{}-{}".format(agentId, entity.id))
        Logger.__pushStatement__("agent_at-{}-{}".format(agentId, entity.id))

        # Action
        Logger.__pushStatement__("!ATTACK-{}-{}".format(agentId, entity.id))

        # Postconditions
        if didKill:
            Logger.__pushStatement__("is_dead-{}".format(entity.id))

        Logger.__pushStatement__("")    # Add a newline

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
