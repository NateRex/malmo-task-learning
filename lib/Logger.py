# ==============================================================================================
# This file exposes functionality for logging traces containing both state and action
# information of a particular agent at regular intervals.
# ==============================================================================================
from datetime import datetime
import os
import time
from Utils import *

class StateFlags(Enum):
    """
    Enumerated type for setting the flags of the Logger class on which state information to track in the initial and final state.
    """
    ClosestMob = 0x00000001
    ClosestPeacefulMob = 0x00000010
    ClosestHostileMob = 0x00000100
    ClosestFoodMob = 0x00001000
    ClosestFoodItem = 0x00010000

class Logger:
    """
    Purely static class containing functionality for logging traces containing state and action information
    as a result of actions performed by a companion agent. All of the methods in this class should be called
    from a corresponding action method, such that the trace output is produced as a direct result of performing
    an action.
    """
    __contents = []                 # The string containing the entire log
    __finalStateContents = []       # List of strings containing final state contents that will not change again
    __declaredEntityIds = []        # A list of entity ids for entities that have already been declared in the log
    __stateFlags = 0x00000000       # A set of flags for determining what information to write out to the initial and final state

    @staticmethod
    def clearTrackingFlags():
        """
        Clears the flags denoting what state information to track in the initial and final states.
        """
        Logger.__stateFlags = 0x00000000

    @staticmethod
    def trackClosestMob():
        """
        Set the flag to track the closest mob of agents in the initial and final state.
        """
        Logger.__stateFlags |= StateFlags.ClosestMob.value

    @staticmethod
    def trackClosestPeacefulMob():
        """
        Set the flag to track the closest peaceful mob of agents in the initial and final state.
        """
        Logger.__stateFlags |= StateFlags.ClosestPeacefulMob.value

    @staticmethod
    def trackClosestHostileMob():
        """
        Set the flag to track the closest hostile mob of agents in the initial and final state.
        """
        Logger.__stateFlags |= StateFlags.ClosestHostileMob.value

    @staticmethod
    def trackClosestFoodMob():
        """
        Set the flag to track the closest food mob of agents in the initial and final state.
        """
        Logger.__stateFlags |= StateFlags.ClosestFoodMob.value

    @staticmethod
    def trackClosestFoodItem():
        """
        Set the flag to track the closest food item of agents in the initial and final state.
        """
        Logger.__stateFlags |= StateFlags.ClosestFoodItem.value

    @staticmethod
    def isTrackingClosestMob():
        """
        Returns true if the Logger is set to track the closest mob of agents in the initial and final state.
        """
        isTracking = Logger.__stateFlags & StateFlags.ClosestMob.value
        if isTracking != 0:
            return True
        else:
            return False

    @staticmethod
    def isTrackingClosestPeacefulMob():
        """
        Returns true if the Logger is set to track the closest peaceful mob of agents in the initial and final state.
        """
        isTracking = Logger.__stateFlags & StateFlags.ClosestPeacefulMob.value
        if isTracking != 0:
            return True
        else:
            return False

    @staticmethod
    def isTrackingClosestHostileMob():
        """
        Returns true if the Logger is set to track the closest hostile mob of agents in the initial and final state.
        """
        isTracking = Logger.__stateFlags & StateFlags.ClosestHostileMob.value
        if isTracking != 0:
            return True
        else:
            return False

    @staticmethod
    def isTrackingClosestFoodMob():
        """
        Returns true if the Logger is set to track the closest food mob of agents in the initial and final state.
        """
        isTracking = Logger.__stateFlags & StateFlags.ClosestFoodMob.value
        if isTracking != 0:
            return True
        else:
            return False

    @staticmethod
    def isTrackingClosestFoodItem():
        """
        Returns true if the Logger is set to track the closest food item of agents in the initial and final state.
        """
        isTracking = Logger.__stateFlags & StateFlags.ClosestFoodItem.value
        if isTracking != 0:
            return True
        else:
            return False

    @staticmethod
    def clearLog():
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
        if agentId in Logger.__declaredEntityIds:   # We already logged this agent
            return

        agentLog = "agents-{}-{}".format(agentId, agentId[:-1])
        Logger.__pushStatement__(agentLog)
        Logger.__finalStateContents.append(agentLog)
        Logger.__declaredEntityIds.append(agentId)

    @staticmethod
    def logItemDefinition(item):
        """
        Internal method that logs the definition of a new item, and adds its id to the list of declared entities.
        """
        if item.id in Logger.__declaredEntityIds:   # We already logged this item
            return

        if isItem(item.type):
            itemLog = "items-{}-{}".format(item.id, item.type)
            Logger.__pushStatement__(itemLog)
            Logger.__finalStateContents.append(itemLog)
            Logger.__declaredEntityIds.append(item.id)

    @staticmethod
    def logMobDefinition(mob):
        """
        Internal method that logs the definition of a new mob, and adds its id to the list of declared entities.
        """
        if mob.id in Logger.__declaredEntityIds:    # We already logged this mob
            return
        
        if isMob(mob.type):
            mobLog = "mobs-{}-{}".format(mob.id, mob.type)
            Logger.__pushStatement__(mobLog)
            Logger.__finalStateContents.append(mobLog)
            Logger.__declaredEntityIds.append(mob.id)

    @staticmethod
    def logEntityDefinition(entity):
        """
        Internal method that logs the definition of any entity, be it item, block, or mob. This adds its id to the list of declared entities.
        """
        if entity.id in Logger.__declaredEntityIds:  # We already logged this entity
            return

        if isMob(entity.type):  # Mob entity
            Logger.logMobDefinition(entity)
        elif isItem(entity.type):   # Item entity
            Logger.logItemDefinition(entity)

    @staticmethod
    def isEntityDefined(entity):
        """
        Returns true if this entity was already previously defined in the log. Returns false otherwise.
        """
        if entity.id in Logger.__declaredEntityIds:
            return True
        return False

    @staticmethod
    def logAgentAquiredItem(agent, item):
        """
        Logs that an agent aquired the item specified.
        """
        agentId = agent.getId()
        Logger.__pushStatement__("agent_has-{}-{}".format(agentId, item.id))

    @staticmethod
    def logAgentLostItem(agent, item):
        """
        Logs that an agent lost the item specified.
        """
        agentId = agent.getId()
        Logger.__pushStatement__("agent_lost-{}-{}".format(agentId, item.id))

    @staticmethod
    def logInitialState(agents):
        """
        Given the list of agents for a mission, log the starting state for the environment in the log.
        """
        for agent in agents:
            agentId = agent.getId()

            # Log the definition of this agent
            Logger.__logAgent__(agent)

            # Log all entities that the agent has identified nearby
            entities = agent.getNearbyEntities()
            if entities != None:
                for entity in entities:
                    Logger.logEntityDefinition(entity)
                    
            # TODO: Starting inventory items

            # Log additional starting data dependent on the Logger flags set (getClosestXXX automatically logs)
            Logger.__pushStatement__("agent_looking_at-{}-{}".format(agentId, ""))
            Logger.__pushStatement__("agent_at-{}-{}".format(agentId, ""))
            if Logger.isTrackingClosestMob():
                agent.getClosestMob()
            if Logger.isTrackingClosestPeacefulMob():
                agent.getClosestPeacefulMob()
            if Logger.isTrackingClosestHostileMob():
                agent.getClosestHostileMob()
            if Logger.isTrackingClosestFoodMob():
                agent.getClosestFoodMob()
            if Logger.isTrackingClosestFoodItem():
                agent.getClosestFoodItem()

        Logger.__pushStatement__("START")
        Logger.__pushNewline__()

    @staticmethod
    def logFinalState(agents):
        """
        Log the end state for the environment in the log.
        """
        Logger.__pushNewline__()
        Logger.__pushStatement__("END")

        # Log any final state information previously recorded as final
        for statement in Logger.__finalStateContents:
            Logger.__pushStatement__(statement)

        # For each agent, log additional data dependent on Logger flags set (getClosestXXX automatically logs)
        for agent in agents:
            agentId = agent.getId()
            Logger.__pushStatement__("agent_looking_at-{}-{}".format(agentId, agent.lastFinishedLookingAt))
            Logger.__pushStatement__("agent_at-{}-{}".format(agentId, agent.lastFinishedMovingTo))
            agent.resetClosestEntityRecords()   # We want to ensure that we re-log despite no change
            if Logger.isTrackingClosestMob():
                agent.getClosestMob()
            if Logger.isTrackingClosestPeacefulMob():
                agent.getClosestPeacefulMob()
            if Logger.isTrackingClosestHostileMob():
                agent.getClosestHostileMob()
            if Logger.isTrackingClosestFoodMob():
                agent.getClosestFoodMob()
            if Logger.isTrackingClosestFoodItem():
                agent.getClosestFoodItem()

    @staticmethod
    def logClosestMob(agent, mob):
        """
        Log the closest mob to the agent given.
        """
        agentId = agent.getId()

        # Special case, where there is no closest mob
        if mob == "":
            if mob != agent.lastClosestMob:
                Logger.__pushStatement__("closest_mob-{}-".format(agentId))
            return

        if not isMob(mob.type):
            return

        # This might be an entity not previously declared in the log. Log its definition if so.
        Logger.logMobDefinition(mob)

        if mob.id != agent.lastClosestMob:
            Logger.__pushStatement__("closest_mob-{}-{}".format(agentId, mob.id))

    @staticmethod
    def logClosestPeacefulMob(agent, mob):
        """
        Log the closest peaceful entity to the agent given.
        """
        agentId = agent.getId()

        # Special case, where there is no closest peaceful mob
        if mob == "":
            if mob != agent.lastClosestPeacefulMob:
                Logger.__pushStatement__("closest_peaceful_mob-{}-".format(agentId))
            return

        if not isPeacefulMob(mob.type):
            return

        # This might be an entity not previously declared in the log. Log its definition if so.
        Logger.logMobDefinition(mob)

        if mob.id != agent.lastClosestPeacefulMob:
            Logger.__pushStatement__("closest_peaceful_mob-{}-{}".format(agentId, mob.id))

    @staticmethod
    def logClosestHostileMob(agent, mob):
        """
        Log the closest hostile entity to the agent given.
        """
        agentId = agent.getId()

        # Special case, where there is no closest hostile mob
        if mob == "":
            if mob != agent.lastClosestHostileMob:
                Logger.__pushStatement__("closest_hostile_mob-{}-".format(agentId))
            return

        if not isHostileMob(mob.type):
            return

        # This might be an entity not previously declared in the log. Log its definition if so.
        Logger.logMobDefinition(mob)

        if mob.id != agent.lastClosestHostileMob:
            Logger.__pushStatement__("closest_hostile_mob-{}-{}".format(agentId, mob.id))

    @staticmethod
    def logClosestFoodMob(agent, mob):
        """
        Log the closest food mob to the agent given.
        """
        agentId = agent.getId()

        # Special case, where there is no closest food mob
        if mob == "":
            if mob != agent.lastClosestFoodMob:
                Logger.__pushStatement__("closest_food_mob-{}-".format(agentId))
            return

        if not isMob(mob.type):
            return
        
        # This might be an entity not previously declared in the log. Log its definition if so.
        Logger.logMobDefinition(mob)

        if mob.id != agent.lastClosestFoodMob:
            Logger.__pushStatement__("closest_food_mob-{}-{}".format(agentId, mob.id))

    @staticmethod
    def logClosestFoodItem(agent, item):
        """
        Log the closest food item to the agent given.
        """
        agentId = agent.getId()

        # Special case, where there is no closest food item
        if item == "":
            if item != agent.lastClosestFoodItem:
                Logger.__pushStatement__("closest_food_item-{}-".format(agentId))
            return

        if not isFoodItem(item.type):
            return

        # This might be an entity not previously declared in the log. Log its definition if so.
        Logger.logItemDefinition(item)

        if item.id != agent.lastClosestFoodItem:
            Logger.__pushStatement__("closest_food_item-{}-{}".format(agentId, item.id))

    __lastLookAtDidFinish = False   # Keep track of whether or not lookAt has finished to log post-conditions ONCE

    @staticmethod
    def logLookAtStart(agent, entity):
        """
        Log the preconditions and action for the LookAt command, provided that it is not a repeat
        call of the previous LookAt command.
        """
        agentId = agent.getId()

        # Ensure this is not a repeat call to do what we were already doing
        if agent.lastStartedLookingAt == entity.id:
            return

        Logger.__pushNewline__()

        # This might be an entity not previously declared in the log. Log it if so.
        Logger.logEntityDefinition(entity)

        # Preconditions - None

        # Action
        Logger.__pushStatement__("!LOOKAT-{}-{}".format(agentId, entity.id))
        Logger.__lastLookAtDidFinish = False

    @staticmethod
    def logLookAtFinish(agent, entity):
        """
        Log the postconditions for the LookAt command, since it has ran to completion before looking elsewhere
        """
        agentId = agent.getId()

        # Did command already run to completion (and was therefore postconditions were logged)?
        if Logger.__lastLookAtDidFinish:
            return

        Logger.__pushStatement__("agent_looking_at-{}-{}".format(agentId, entity.id))
        Logger.__lastLookAtDidFinish = True
        Logger.__pushNewline__()

    __lastMoveToDidFinish = False   # Keep track of whether or not moveTo has finished to log post-conditions ONCE
    
    @staticmethod
    def logMoveToStart(agent, entity):
        """
        Log the preconditions and action for the MoveTo command, provided that it is not a repeat
        call of the previous LookAt command.
        """
        agentId = agent.getId()

        # Ensure this is not a repeat call to do what we were already doing
        if agent.lastStartedMovingTo == entity.id:
            return

        Logger.__pushNewline__()

        # This might be an entity not previously declared in the log. Log it if so.
        Logger.logEntityDefinition(entity)

        # Pre-conditions
        Logger.__pushStatement__("agent_looking_at-{}-{}".format(agentId, entity.id))

        # Action
        Logger.__pushStatement__("!MOVETO-{}-{}".format(agentId, entity.id))
        Logger.__lastMoveToDidFinish = False

    @staticmethod
    def logMoveToFinish(agent, entity):
        """
        Log the postconditions for the MoveTo command, since it has ran to completion before moving elsewhere.
        """
        agentId = agent.getId()

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

        Logger.__pushNewline__()

        # Preconditions
        for item in itemsUsed:
            Logger.logAgentAquiredItem(agent, item)

        # Action
        Logger.__pushStatement__("!CRAFT-{}-{}".format(agentId, itemCrafted.type))

        # Postconditions
        Logger.__pushStatement__("items-{}-{}".format(itemCrafted.type, itemCrafted.id))
        Logger.logAgentAquiredItem(agent, itemCrafted)
        for item in itemsUsed:
            Logger.logAgentLostItem(agent, item)

        Logger.__pushNewline__()
        

    __lastAttack = None     # Keep track of the last entity we attacked to avoid unnecessary repeat logs

    @staticmethod
    def logAttack(agent, entity, didKill):
        """
        Log the preconditions, action, and possible postconditions for the Attack command.
        """
        agentId = agent.getId()

        Logger.__pushNewline__()

        # Preconditions
        Logger.__pushStatement__("agent_looking_at-{}-{}".format(agentId, entity.id))
        Logger.__pushStatement__("agent_at-{}-{}".format(agentId, entity.id))

        # Action
        Logger.__pushStatement__("!ATTACK-{}-{}".format(agentId, entity.id))

        # Postconditions
        if didKill:
            deadLog = "is_dead-{}".format(entity.id)
            Logger.__pushStatement__(deadLog)
            Logger.__finalStateContents.append(deadLog)

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
        Logger.logAgentAquiredItem(sourceAgent, item)

        # Action
        Logger.__pushStatement__("!GIVEITEM-{}-{}-{}".format(sourceAgentId, item.id, targetAgentId))

        # Postconditions
        Logger.logAgentLostItem(sourceAgent, item)
        Logger.logAgentAquiredItem(targetAgent, item)

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
        with open(filePath, "w+") as logFile:
            logFile.write("\n".join(Logger.__contents))
        print("Mission log output has been saved to: " + filePath)
        Logger.clearLog()
