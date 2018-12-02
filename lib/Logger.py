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
    __contents = []                 # The string containing the entire log
    __declaredEntityIds = []        # A list of entity ids for entities that have already been declared in the log
    __needNewline = True            # Whether or not a newline is needed before logging a new action

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
        Logger.__contents.append(value)

    @staticmethod
    def __pushNewline__():
        """
        Ensures that the previous statement is a newline, otherwise, appends one.
        """
        if len(Logger.__contents) == 0:
            return
        if Logger.__needNewline and Logger.__contents[len(Logger.__contents) - 1] != "":
            Logger.__contents.append("")
        Logger.__needNewline = True

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
    def logNewItem(item):
        """
        Internal method that logs the definition of a new item, and adds its id to the list of declared entities.
        """
        if item.id in Logger.__declaredEntityIds:   # We already logged this item
            return

        if item.type in ItemType.All.__members__:
            Logger.__pushStatement__("items-{}-{}".format(item.type, item.id))
            Logger.__declaredEntityIds.append(item.id)
        
        Logger.__needNewline = False

    @staticmethod
    def __logMob__(mob):
        """
        Internal method that logs the definition of a new mob, and adds its id to the list of declared entities.
        """
        if mob.id in Logger.__declaredEntityIds:    # We already logged this mob
            return
        
        if mob.type in MobType.All.__members__:
            Logger.__pushStatement__("mobs-{}-{}".format(mob.type, mob.id))
            Logger.__declaredEntityIds.append(mob.id)
        
        Logger.__needNewline = False

    @staticmethod
    def __logEntity__(entity):
        """
        Internal method that logs the definition of a new entity, and adds its id to the list of declared entities.
        """
        if entity.id in Logger.__declaredEntityIds:  # We already logged this entity
            return

        if entity.type in MobType.All.__members__:
            Logger.__logMob__(entity)
        elif entity.type in ItemType.All.__members__:
            Logger.logNewItem(entity)
        
        Logger.__needNewline = False

    @staticmethod
    def __logAgentInventory__(agent):
        """
        Internal method that logs everything that an agent has in their inventory.
        """
        agentId = agent.getId()
        agentInventoryJson = agent.getInventoryJson()
        if agentId == None or agentInventoryJson == None:
            return

        agent.inventory.update(agentInventoryJson)    # Make sure this agent's inventory is up-to-date
        items = agent.inventory.getAllItems()

        for item in items:
            Logger.logNewItem(item)    # We might not have logged this item yet
            Logger.__pushStatement__("agent_has-{}-{}".format(agentId, item.id))

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

        Logger.__pushStatement__("START")
        Logger.__pushNewline__()

    @staticmethod
    def logFinalState():
        """
        Log the end state for the environment in the log.
        """
        Logger.__pushNewline__()
        Logger.__pushStatement__("END")

    __lastClosestMob = None

    @staticmethod
    def logClosestMob(agent, mob):
        """
        Log the closest mob to the agent given.
        """
        if mob.type not in MobType.All.__members__:
            return
        agentId = agent.getId()
        if agentId == None:
            return

        # This might be an entity not previously declared in the log. Log it if so.
        Logger.__logMob__(mob)

        if Logger.__lastClosestMob == None or mob.id != Logger.__lastClosestMob.id:
            Logger.__pushStatement__("closest_mob-{}-{}-{}".format(agentId, mob.type, mob.id))
            Logger.__lastClosestMob = mob

        Logger.__needNewline = False

    __lastClosestPeacefulMob = None

    @staticmethod
    def logClosestPeacefulMob(agent, mob):
        """
        Log the closest peaceful entity to the agent given.
        """
        if mob.type not in MobType.Peaceful.__members__:
            return
        agentId = agent.getId()
        if agentId == None:
            return

        # This might be an entity not previously declared in the log. Log it if so.
        Logger.__logMob__(mob)

        if Logger.__lastClosestPeacefulMob == None or mob.id != Logger.__lastClosestPeacefulMob.id:
            Logger.__pushStatement__("closest_peaceful_mob-{}-{}-{}".format(agentId, mob.type, mob.id))
            Logger.__lastClosestPeacefulMob = mob

        Logger.__needNewline = False

    __lastClosestHarmfulMob = None

    @staticmethod
    def logClosestHarmfulMob(agent, mob):
        """
        Log the closest harmful entity to the agent given.
        """
        if mob.type not in MobType.Hostile.__members__:
            return
        agentId = agent.getId()
        if agentId == None:
            return

        # This might be an entity not previously declared in the log. Log it if so.
        Logger.__logMob__(mob)

        if Logger.__lastClosestHarmfulMob == None or mob.id != Logger.__lastClosestHarmfulMob.id:
            Logger.__pushStatement__("closest_harmful_mob-{}-{}-{}".format(agentId, mob.type, mob.id))
            Logger.__lastClosestHarmfulMob = mob

        Logger.__needNewline = False

    __lastClosestFoodMob = None

    @staticmethod
    def logClosestFoodMob(agent, mob):
        """
        Log the closest food mob to the agent given.
        """
        if mob.type not in MobType.Food.__members__:
            return
        agentId = agent.getId()
        if agentId == None:
            return
        
        # This might be an entity not previously declared in the log. Log it if so.
        Logger.__logMob__(mob)

        if Logger.__lastClosestFoodMob == None or mob.id != Logger.__lastClosestFoodMob.id:
            Logger.__pushStatement__("closest_food_mob-{}-{}-{}".format(agentId, mob.type, mob.id))
            Logger.__lastClosestFoodMob = mob

        Logger.__needNewline = False

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

        Logger.__pushNewline__()

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
        Logger.__lastLookAtDidFinish = True
        Logger.__pushNewline__()

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

        Logger.__pushNewline__()

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
        Logger.__lastMoveToDidFinish = True
        Logger.__pushNewline__()

    @staticmethod
    def logCraft(agent, itemCrafted, itemsUsed):
        """
        Log the preconditions, action, and postconditions for the Craft command.
        """
        agentId = agent.getId()
        if agentId == None:
            return

        Logger.__pushNewline__()

        # Preconditions
        for item in itemsUsed:
            Logger.__pushStatement__("agent_has-{}-{}".format(agentId, item.id))

        # Action
        Logger.__pushStatement__("!CRAFT-{}-{}".format(agentId, itemCrafted.type))

        # Postconditions
        Logger.__pushStatement__("items-{}-{}".format(itemCrafted.type, itemCrafted.id))
        Logger.__pushStatement__("agent_has-{}-{}".format(agentId, itemCrafted.id))
        for item in itemsUsed:
            Logger.__pushStatement__("agent_lost-{}-{}".format(agentId, item.id))

        Logger.__pushNewline__()
        

    __lastAttack = None     # Keep track of the last entity we attacked to avoid unnecessary repeat logs

    @staticmethod
    def logAttack(agent, entity, didKill):
        """
        Log the preconditions, action, and possible postconditions for the Attack command.
        """
        agentId = agent.getId()
        if agentId == None:
            return

        Logger.__pushNewline__()

        # Preconditions
        Logger.__pushStatement__("agent_looking_at-{}-{}".format(agentId, entity.id))
        Logger.__pushStatement__("agent_at-{}-{}".format(agentId, entity.id))

        # Action
        Logger.__pushStatement__("!ATTACK-{}-{}".format(agentId, entity.id))

        # Postconditions
        if didKill:
            Logger.__pushStatement__("is_dead-{}".format(entity.id))

        Logger.__pushNewline__()

    @staticmethod
    def logGiveItemToAgent(sourceAgent, item, targetAgent):
        """
        Log the preconditions, action, and possible postconditions for the GiveItem command.
        """
        sourceAgentId = sourceAgent.getId()
        targetAgentId = targetAgent.getId()
        if sourceAgentId == None or targetAgentId == None:
            return

        Logger.__pushNewline__()

        # Preconditions
        Logger.__pushStatement__("agent_looking_at-{}-{}".format(sourceAgentId, targetAgentId))
        Logger.__pushStatement__("agent_at-{}-{}".format(sourceAgentId, targetAgentId))
        Logger.__pushStatement__("agent_has-{}-{}".format(sourceAgentId, item.id))

        # Action
        Logger.__pushStatement__("!GIVEITEM-{}-{}-{}".format(sourceAgentId, item.id, targetAgentId))

        # Postconditions
        Logger.__pushStatement__("agent_lost-{}-{}".format(sourceAgentId, item.id))
        Logger.__pushStatement__("agent_has-{}-{}".format(targetAgentId, item.id))

        Logger.__pushNewline__()

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
        logFile.write("\n".join(Logger.__contents))
        logFile.close()
        print("Mission log output has been saved to: " + filePath)
        Logger.clear()
