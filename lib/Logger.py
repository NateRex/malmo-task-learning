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
        if Logger.__contents[len(Logger.__contents) - 1] != "":
            Logger.__contents.append("")

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
    def logItem(item):
        """
        Internal method that logs the definition of a new item, and adds its id to the list of declared entities.
        """
        if item.id in Logger.__declaredEntityIds:   # We already logged this item
            return

        if item.type in ItemType.All.__members__:
            Logger.__pushStatement__("items-{}-{}".format(item.type, item.id))
            Logger.__declaredEntityIds.append(item.id)

    @staticmethod
    def logMob(mob):
        """
        Internal method that logs the definition of a new mob, and adds its id to the list of declared entities.
        """
        if mob.id in Logger.__declaredEntityIds:    # We already logged this mob
            return
        
        if mob.type in MobType.All.__members__:
            Logger.__pushStatement__("mobs-{}-{}".format(mob.type, mob.id))
            Logger.__declaredEntityIds.append(mob.id)

    @staticmethod
    def logEntity(entity):
        """
        Internal method that logs the definition of a new entity, and adds its id to the list of declared entities.
        """
        if entity.id in Logger.__declaredEntityIds:  # We already logged this entity
            return

        if entity.type in MobType.All.__members__:  # Mob entity
            Logger.logMob(entity)
        elif entity.type in ItemType.All.__members__:   # Item entity
            Logger.logItem(entity)

    @staticmethod
    def logAquiredItem(agent, item):
        """
        Logs that an agent aquired the item specified.
        """
        agentId = agent.getId()
        if agentId == None:
            return
        Logger.__pushStatement__("agent_has-{}-{}".format(agentId, item.id))

    @staticmethod
    def logLostItem(agent, item):
        """
        Logs that an agent lost the item specified.
        """
        agentId = agent.getId()
        if agentId == None:
            return
        Logger.__pushStatement__("agent_lost-{}-{}".format(agentId, item.id))

    @staticmethod
    def logInitialState(agents):
        """
        Given the list of agents for a mission, log the starting state for the environment in the log.
        """
        for agent in agents:
            # Log the definition of this agent
            Logger.__logAgent__(agent)

            # Log all entities that the agent has identified nearby
            entities = agent.getNearbyEntities()
            if entities != None:
                for entity in entities:
                    Logger.logEntity(entity)
                    
            # Note: Logging for agent inventory is managed from AgentInventory class

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
        Logger.logMob(mob)

        if Logger.__lastClosestMob == None or mob.id != Logger.__lastClosestMob.id:
            Logger.__pushStatement__("closest_mob-{}-{}-{}".format(agentId, mob.type, mob.id))
            Logger.__lastClosestMob = mob

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
        Logger.logMob(mob)

        if Logger.__lastClosestPeacefulMob == None or mob.id != Logger.__lastClosestPeacefulMob.id:
            Logger.__pushStatement__("closest_peaceful_mob-{}-{}-{}".format(agentId, mob.type, mob.id))
            Logger.__lastClosestPeacefulMob = mob

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
        Logger.logMob(mob)

        if Logger.__lastClosestHarmfulMob == None or mob.id != Logger.__lastClosestHarmfulMob.id:
            Logger.__pushStatement__("closest_harmful_mob-{}-{}-{}".format(agentId, mob.type, mob.id))
            Logger.__lastClosestHarmfulMob = mob

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
        Logger.logMob(mob)

        if Logger.__lastClosestFoodMob == None or mob.id != Logger.__lastClosestFoodMob.id:
            Logger.__pushStatement__("closest_food_mob-{}-{}-{}".format(agentId, mob.type, mob.id))
            Logger.__lastClosestFoodMob = mob

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
        Logger.logEntity(entity)

        # Preconditions - None

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
        Logger.logEntity(entity)

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
            Logger.logAquiredItem(agent, item)

        # Action
        Logger.__pushStatement__("!CRAFT-{}-{}".format(agentId, itemCrafted.type))

        # Postconditions
        Logger.__pushStatement__("items-{}-{}".format(itemCrafted.type, itemCrafted.id))
        Logger.logAquiredItem(agent, itemCrafted)
        for item in itemsUsed:
            Logger.logLostItem(agent, item)

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
        Logger.logAquiredItem(sourceAgent, item)

        # Action
        Logger.__pushStatement__("!GIVEITEM-{}-{}-{}".format(sourceAgentId, item.id, targetAgentId))

        # Postconditions
        Logger.logLostItem(sourceAgent, item)
        Logger.logAquiredItem(targetAgent, item)

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
