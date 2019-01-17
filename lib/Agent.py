# ==============================================================================================
# This file contains wrapper classes and functionality relating to a Malmo agent. This combines
# several primitive commands into larger commands that can be used to acheive more complex tasks.
# Logging is also handled automatically for each command that creates a corresponding trace.
# ==============================================================================================
import MalmoPython
import json
import math
import time
from Utils import *
from Logger import *
from AgentInventory import *
from Stats import *

class Agent:
    """
    Wrapper class for a Malmo agent for executing complex commands with corresponding logging.
    To access the Malmo AgentHost object, use the 'host' member.
    """
    agentList = []  # A list of all agents that have been created

    def __init__(self, name):
        self.host = MalmoPython.AgentHost()     # A reference to a Malmo AgentHost object
        self.inventory = AgentInventory(self)   # This agent's inventory
        self.stats = Stats(self)                # This agent's statistical information
        self.id = "{}1".format(name)            # The ID of this agent
        self.actionOverride = None              # An function pointer that, if present, is ran instead of any called actions
        Agent.agentList.append(self)            # Add this agent to the global list of all agents

        # Recorded information for previous state/action observations used for checking state changes and logging
        self.lastWorldState = None
        self.lastStartedLookingAt = ""
        self.lastFinishedLookingAt = ""
        self.lastStartedMovingTo = ""
        self.lastFinishedMovingTo = ""
        self.lastClosestMob = None
        self.lastClosestPeacefulMob = None
        self.lastClosestHostileMob = None
        self.lastClosestFoodMob = None
        self.lastClosestFoodItem = None
        self.lastItemAmount = 0

    @staticmethod
    def findAgentById(agentId):
        """
        Searches through the list of agents that have been created, and returns an agent with the id given.
        If no agent exists with that id, returns None.
        """
        for agent in Agent.agentList:
            if agent.id == agentId:
                return agent
        return None

    def resetClosestEntityRecords(self):
        """
        Resets the information regarding the most recent entities found nearby.
        """
        self.lastClosestMob = None
        self.lastClosestPeacefulMob = None
        self.lastClosestHostileMob = None
        self.lastClosestFoodMob = None
        self.lastClosestFoodItem = None

    def isMissionActive(self):
        """
        Returns true if this agent's mission is still running.
        """
        return self.host.peekWorldState().is_mission_running

    def getObservationJson(self):
        """
        Returns the entire world state containing the most recent observations as a JSON object.
        """
        agentState = self.host.getWorldState()
        if len(agentState.observations) > 0:
            self.lastWorldState = json.loads(agentState.observations[-1].text)
        return self.lastWorldState

    def getId(self):
        """
        Returns the unique identifier for this agent. Returns none if unsuccessful.
        """
        return self.id

    def getPosition(self):
        """
        Returns the Vector position of this agent.
        If no observations have occurred, returns None.
        """
        agentState = self.getObservationJson()
        if agentState == None:
            return None
        return Vector(agentState["XPos"], agentState["YPos"] + 1, agentState["ZPos"])   # Agent's head is above the agent's location

    def getDamageDealt(self):
        """
        Returns the amount of damage this agent has dealt out to other entities.
        If no observations have occurred, returns None.
        """
        agentState = self.getObservationJson()
        if agentState == None:
            return None
        return agentState["DamageDealt"]

    def getMobsKilled(self):
        """
        Returns the number of mobs this agent has killed.
        If no observations have occurred, returns None.
        """
        agentState = self.getObservationJson()
        if agentState == None:
            return None
        return agentState["MobsKilled"]

    def getPlayersKilled(self):
        """
        Returns the number of players this agent has killed.
        If no observations have occured, returns None.
        """
        agentState = self.getObservationJson()
        if agentState == None:
            return None
        return agentState["PlayersKilled"]

    def getTimeAlive(self):
        """
        Returns the time the agent has been alive for
        If no observations have occured, returns None.
        """
        agentState = self.getObservationJson()
        if agentState == None:
            return None
        return agentState["TimeAlive"]

    def getScore(self):
        """
        Returns the score of the agent.
        If no observations have occured, returns None.
        """
        agentState = self.getObservationJson()
        if agentState == None:
            return None
        return agentState["Score"]

    def getXP(self):
        """
        Returns the xp of the agent.
        If no observations have occured, returns None.
        """
        agentState = self.getObservationJson()
        if agentState == None:
            return None
        return agentState["XP"]

    def getDistanceTravelled(self):
        """
        Returns the distance travelled by the agent.
        If no observations have occured, returns None.
        """
        agentState = self.getObservationJson()
        if agentState == None:
            return None
        return agentState["DistanceTravelled"]

    def getHealth(self):
        """
        Returns the current health of the agent.
        """
        agentState = self.getObservationJson()
        if agentState == None:
            return None
        return agentState["Life"]

    def getHunger(self):
        """
        Returns the current hunger of the agent.
        """
        agentState = self.getObservationJson()
        if agentState == None:
            return None
        return agentState["Food"]

    def getInventoryJson(self):
        """
        Returns an array of JSON inventory items that this agent is currently carrying.
        If no observations have occurred, returns None.
        """
        agentState = self.getObservationJson()
        if agentState == None:
            return None
        return agentState["inventory"]

    def getCurrentHotbarIndex(self):
        """
        Returns the hotbar index (0-based) that this agent currently has selected.
        If unable to determine the currently used hotbar index, returns -1.
        """
        agentState = self.getObservationJson()
        if agentState == None:
            return -1
        return agentState["currentItemIndex"]

    def __getNextAvailableHotbarIndex__(self):
        """
        Internal method that returns the next hotbar index (0-based) that is empty.
        If there is no such slot available, returns -1.
        """
        inventory = self.getInventoryJson()
        if inventory == None:
            return -1

        # Record all used hotbar index
        usedSlots = []
        for i in range(0, len(inventory)):
            currentItem = inventory[i]
            if currentItem["index"] < 9:
                usedSlots.append(currentItem["index"])

        # Now find first hotbar index not in use
        for i in range(0, 9):
            if not i in usedSlots:
                return i
        return -1

    def __locationOfItemInInventory__(self, item):
        """
        Internal method that returns the inventory index of the specified item in this agent's inventory.
        Returns -1 if the agent does not carry that item.
        """
        inventory = self.getInventoryJson()
        if inventory == None:
            return -1
        
        for i in range(0, len(inventory)):
            currentItem = inventory[i]
            if currentItem["type"] == item.value:
                return currentItem["index"] 
        return -1

    def __startMoving__(self, speed):
        """
        Start moving backwards or forwards at a specific speed. Accepted values range from -1 to 1.
        """
        self.host.sendCommand("move {}".format(speed))

    def stopMoving(self):
        """
        Stop moving forwards/backwards.
        """
        self.host.sendCommand("move 0")

    def __startStrafing__(self, speed):
        """
        Start moving left or right continuously at a specific speed. Accepted values range from -1 to 1.
        """
        self.host.sendCommand("strafe {}".format(speed))

    def __stopStrafing__(self, speed):
        """
        Stop moving left/right.
        """
        self.host.sendCommand("strafe 0")

    def __startChangingPitch__(self, speed):
        """
        Start tilting the agent's head up or down continuously at a specific speed. Accepted values range from -1 to 1.
        """
        self.host.sendCommand("pitch {}".format(speed))

    def __stopChangingPitch__(self):
        """
        Stop tilting the agent's head up/down.
        """
        self.host.sendCommand("pitch 0")

    def __startChangingYaw__(self, speed):
        """
        Start turning continuously to the left or right at a specific speed. Accepted values range from -1 to 1.
        """
        self.host.sendCommand("turn {}".format(speed))

    def __stopChangingYaw__(self):
        """
        Stop turning left/right.
        """
        self.host.sendCommand("turn 0")
    
    def stopTurning(self):
        """
        Stop turning left/right and up/down.
        """
        self.__stopChangingYaw__()
        self.__stopChangingPitch__()

    def __startJumping__(self):
        """
        Start jumping continuously.
        """
        self.host.sendCommand("jump 1")

    def __stopJumping__(self):
        """
        Stop jumping.
        """
        self.host.sendCommand("jump 0")

    def __startCrouching__(self):
        """
        Start crouching continuously.
        """
        self.host.sendCommand("crouch 1")

    def __stopCrouching__(self):
        """
        Stop crouching.
        """
        self.host.sendCommand("crouch 0")

    def __startAttacking__(self):
        """
        Start attacking continuously.
        """
        self.host.sendCommand("attack 1")

    def stopAttacking(self):
        """
        Stop attacking.
        """
        self.host.sendCommand("attack 0")

    def __startUsingItem__(self):
        """
        Begin continuously using the item in the currently selected hotbar slot.
        """
        self.host.sendCommand("use 1")

    def __stopUsingItem__(self):
        """
        Stop using the item in the currently selected hotbar slot.
        """
        self.host.sendCommand("use 0")

    def __throwItem__(self):
        """
        Throws item currently equipped.
        """
        self.host.sendCommand("discardCurrentItem")

    def stopAllMovement(self):
        """
        Stops any form of movement by this agent, including yaw/pitch turning and walking.
        """
        self.stopTurning()
        self.stopMoving()
        self.stopAttacking()

    def getNearbyEntities(self):
        """
        Returns a list of named EntityInfo tuples of all entities within a 20x20 area around this agent.
        Returns None on error.
        """
        worldState = self.getObservationJson()
        if worldState == None:
            return None
        entities = [EntityInfo("{}{}".format(k["name"], numerifyId(k["id"]).replace("-", "")), k["name"], Vector(k["x"], k["y"], k["z"]), k.get("quantity")) for k in worldState["nearby_entities"]]
        return entities

    def getNearbyEntityById(self, entityId):
        """
        Returns a named EntityInfo tuple describing an entity near this agent, using its id. If an entity with that id is not found, returns None.
        """
        entities = self.getNearbyEntities()
        for entity in entities:
            if entity.id == entityId:
                return entity
        return None

    def getClosestMob(self):
        """
        Returns a named EntityInfo tuple of the nearest mob within a 20x20 area of this agent.
        Returns none if no such mob exists.
        """
        agentPos = self.getPosition()
        entities = self.getNearbyEntities()
        if agentPos == None or entities == None:
            return None
        nearestDistance = 1000000
        nearestEntity = None
        for entity in entities:   # First entity is always the agent itself
            if isMob(entity.type):
                entityPos = entity.position
                distanceToEntity = MathExt.distanceBetweenPoints(agentPos, entityPos)
                if distanceToEntity < nearestDistance:
                    nearestDistance = distanceToEntity
                    nearestEntity = entity
        if nearestEntity == None:
            Logger.logClosestMob(self, "")
            self.lastClosestMob = ""
            return None
        Logger.logMobDefinition(nearestEntity)    # In case we never saw this entity before
        Logger.logClosestMob(self, nearestEntity)
        self.lastClosestMob = nearestEntity.id
        return nearestEntity

    def getClosestPeacefulMob(self):
        """
        Returns a named EntityInfo tuple of the nearest peaceful mob within a 20x20 area of this agent.
        Returns None if no such mob exists.
        """
        agentPos = self.getPosition()
        entities = self.getNearbyEntities()
        if agentPos == None or entities == None:
            return None
        nearestDistance = 1000000
        nearestEntity = None
        for entity in entities:
            if isPeacefulMob(entity.type):
                entityPos = entity.position
                distanceToEntity = MathExt.distanceBetweenPoints(agentPos, entityPos)
                if distanceToEntity < nearestDistance:
                    nearestDistance = distanceToEntity
                    nearestEntity = entity
        if nearestEntity == None:
            Logger.logClosestPeacefulMob(self, "")
            self.lastClosestPeacefulMob = ""
            return None
        Logger.logMobDefinition(nearestEntity)    # In case we never saw this entity before
        Logger.logClosestPeacefulMob(self, nearestEntity)
        self.lastClosestPeacefulMob = nearestEntity.id
        return nearestEntity

    def getClosestHostileMob(self):
        """
        Returns a named EntityInfo tuple of the nearest harmful mob within a 20x20 area of this agent.
        Returns None if no such mob exists.
        """
        agentPos = self.getPosition()
        entities = self.getNearbyEntities()
        if agentPos == None or entities == None:
            return None
        nearestDistance = 1000000
        nearestEntity = None
        for entity in entities:
            if isHostileMob(entity.type):
                entityPos = entity.position
                distanceToEntity = MathExt.distanceBetweenPoints(agentPos, entityPos)
                if distanceToEntity < nearestDistance:
                    nearestDistance = distanceToEntity
                    nearestEntity = entity
        if nearestEntity == None:
            Logger.logClosestHostileMob(self, "")
            self.lastClosestHostileMob = ""
            return None
        Logger.logMobDefinition(nearestEntity)    # In case we never saw this entity before
        Logger.logClosestHostileMob(self, nearestEntity)
        self.lastClosestHostileMob = nearestEntity.id
        return nearestEntity

    def getClosestFoodMob(self):
        """
        Returns a named EntityInfo tuple of the nearest food mob within a 20x20 area of this agent.
        Returns None if no such mob exists.
        """
        agentPos = self.getPosition()
        entities = self.getNearbyEntities()
        if agentPos == None or entities == None:
            return None
        nearestDistance = 1000000
        nearestEntity = None
        for entity in entities:
            if isFoodMob(entity.type):
                entityPos = entity.position
                distanceToEntity = MathExt.distanceBetweenPoints(agentPos, entityPos)
                if distanceToEntity < nearestDistance:
                    nearestDistance = distanceToEntity
                    nearestEntity = entity
        if nearestEntity == None:
            Logger.logClosestFoodMob(self, "")
            self.lastClosestFoodMob = ""
            return None
        Logger.logMobDefinition(nearestEntity)    # In case we never saw this entity before
        Logger.logClosestFoodMob(self, nearestEntity)
        self.lastClosestFoodMob = nearestEntity.id
        return nearestEntity

    def getClosestFoodItem(self):
        """
        Returns a named EntityInfo tuple of the nearest food item within a 20x20 area of this agent.
        Returns None if no such item exists.
        """
        agentPos = self.getPosition()
        entities = self.getNearbyEntities()
        if agentPos == None or entities == None:
            return None
        nearestDistance = 1000000
        nearestEntity = None
        for entity in entities:
            if isFoodItem(entity.type):
                entityPos = entity.position
                distanceToEntity = MathExt.distanceBetweenPoints(agentPos, entityPos)
                if distanceToEntity < nearestDistance:
                    nearestDistance = distanceToEntity
                    nearestEntity = entity
        if nearestEntity == None:
            Logger.logClosestFoodItem(self, "")
            self.lastClosestFoodItem = ""
            return None

        # If we did not log this entity definition, we must do so for it, as well as all other items in the stack of items
        if not Logger.isEntityDefined(nearestEntity):
            Logger.logItemDefinition(nearestEntity)
            AgentInventory.enqueueItemId(nearestEntity)
            for _ in range(1, nearestEntity.quantity):
                newItem = Item("{}{}".format(nearestEntity.type, self.inventory.getId()), nearestEntity.type)
                Logger.logItemDefinition(newItem)
                AgentInventory.enqueueItemId(newItem)
        Logger.logClosestFoodItem(self, nearestEntity)
        self.lastClosestFoodItem = nearestEntity.id
        return nearestEntity

    def getClosestBlockLocation(self, blockType):
        """
        Returns the nearest block of a given type as an entity.
        """
        agentState = self.getObservationJson()
        if agentState == None:
            return self.getPosition
        currentPos = self.getPosition()

        # Get observation grid of nearby blocks
        grid = agentState.get(u'floor11x11', 0)

        # The number of the block in the grid
        block = 200
        x = 200
        y = 200
        z = 200
        for i in range(0, 363):
            # If a block of a given type is found
            if grid[i] == blockType.value:
                tempX = (i % 11) - 5
                tempY = -1
                tempZ = ((i - (i%11)) / 11) % 11 - 5
                if i > 120 and i < 241:
                    tempY = 0
                elif i > 240:
                    tempY = 1

                # If new block is closer to companion than the previous one, return this block
                if (abs(tempX) + abs(tempZ)) + abs(tempY) < (abs(x) + abs(z)) + abs(tempY):
                    block = i
                    x = tempX
                    y = tempY
                    z = tempZ

        # If no block is found, return none
        if block == 200:
            return None

        # Calculate the position of the block and return it as an entity
        x = x + currentPos.x - (currentPos.x % 1) + 0.5
        y = y + currentPos.y - (currentPos.y % 1) - 1
        z = z + currentPos.z - (currentPos.z % 1) + 0.5
        blockPos = Vector(x, y, z)
        blockEnt = EntityInfo(blockType.value + str(blockPos.x) + str(blockPos.y) + str(blockPos.z), blockType.value, blockPos, 1)
        return blockEnt

    def __getYawRateToFacePosition__(self, targetPosition):
        """
        Obtain a rate in which to turn along the yaw angle to face a given target position.
        """
        worldState = self.getObservationJson()
        agentPos = self.getPosition()
        if worldState == None or agentPos == None:
            return False    
        currentAngle = worldState["Yaw"] if worldState["Yaw"] >= 0 else 360.0 - abs(worldState["Yaw"])
        vector = MathExt.vectorFromPoints(agentPos, targetPosition)
        vector = MathExt.normalizeVector(vector)

        # Get the angle that we wish to face
        targetAngle = None
        if MathExt.valuesAreEqual(vector.x, 0, 1.0e-14): # Avoid dividing by 0
            if vector.z >= 0:
                targetAngle = -MathExt.PI_OVER_TWO
            else:
                targetAngle = MathExt.PI_OVER_TWO
        else:
            targetAngle = math.atan(vector.z / vector.x)
    
        # Adjust angle based on quadrant of vector
        if vector.x <= 0:   # Quadrant 1 or 2
            targetAngle = MathExt.PI_OVER_TWO + targetAngle
        elif vector.x > 0:  # Quadrant 3 or 4
            targetAngle = MathExt.THREE_PI_OVER_TWO + targetAngle

        targetAngle = math.degrees(targetAngle)
        if MathExt.valuesAreEqual(targetAngle, 360.0, 1.0e-14):
            targetAngle = 0

        # Get difference between the two angles
        diff = None
        if currentAngle <= targetAngle:
            diff = min(targetAngle - currentAngle, 360 - targetAngle + currentAngle)
        else:
            diff = min(currentAngle - targetAngle, 360 - currentAngle + targetAngle)
        
        # Get the turning direction
        multiplier = 1
        if currentAngle > targetAngle and currentAngle - targetAngle < 180:
            multiplier = -1
        elif targetAngle > currentAngle and targetAngle - currentAngle > 180:
            multiplier = -1

        # Get the turning rate
        rate = 0
        if diff > 10:
            rate = 1.0 * multiplier
        elif diff > 5:
            rate = .25 * multiplier
        elif diff > 2:
            rate = .05 * multiplier
        else:
            rate = MathExt.affineTransformation(diff, 0.0, 180.0, 0, 1.0) * multiplier

        return rate

    def __getPitchRateToFacePosition__(self, targetPosition):
        """
        Obtain a rate in which to turn along the pitch angle to face the given target position.
        """
        worldState = self.getObservationJson()
        agentPos = self.getPosition()
        if worldState == None or agentPos == None:
            return False  
        currentAngle = worldState["Pitch"]
        vectorWithHeight = MathExt.vectorFromPoints(agentPos, targetPosition)
        vectorWithHeight = MathExt.normalizeVector(vectorWithHeight)
        vectorWithoutHeight = Vector(vectorWithHeight.x, 0, vectorWithHeight.z)

        # Get the angle that we wish to change the pitch to (account for range -90 to 90)
        if MathExt.isZeroVector(vectorWithHeight) or MathExt.isZeroVector(vectorWithoutHeight): # Avoid dividing by 0
            return False
        cosValue = MathExt.dotProduct(vectorWithHeight, vectorWithoutHeight) / (MathExt.vectorMagnitude(vectorWithHeight) * MathExt.vectorMagnitude(vectorWithoutHeight))
        if cosValue > 1:
            cosValue = 1
        elif cosValue < -1:
            cosValue = -1
        targetAngle = math.acos(cosValue)
        if vectorWithHeight.y > 0:
            targetAngle = -targetAngle

        targetAngle = math.degrees(targetAngle)

        # Get difference between two angles
        diff = None
        if currentAngle <= targetAngle:
            diff = targetAngle - currentAngle
        else:
            diff = currentAngle - targetAngle

        # Get the turning direction
        multiplier = 1
        if currentAngle > targetAngle:
            multiplier = -1

        # Get the turning rate
        rate = 0
        if diff > 10:
            rate = 1.0 * multiplier
        elif diff > 5:
            rate = .25 * multiplier
        elif diff > 2:
            rate = .05 * multiplier
        else:
            rate = MathExt.affineTransformation(diff, 0.0, 180.0, 0, 1.0) * multiplier
        return rate

    def __isLookingAt__(self, targetPosition):
        """
        Returns true if this agent is currently looking in the proximity of the target position.
        """
        # Our tolerance depends on how close we are to the object
        agentPos = self.getPosition()
        distanceFromTarget = MathExt.distanceBetweenPoints(agentPos, targetPosition)
        yawRate = self.__getYawRateToFacePosition__(targetPosition)
        pitchRate = self.__getPitchRateToFacePosition__(targetPosition)
        if distanceFromTarget > 7:
            if abs(yawRate) >= .25 or abs(pitchRate) >= .25:
                return False
        else:
            if abs(yawRate) >= .8 or abs(pitchRate) >= .8:
                return False
        return True

    def __lookAtPosition__(self, targetPosition):
        """
        Begin continuously turning/looking to face a Vector position.
        Returns true if the agent is currently looking at the target. Returns false otherwise.
        """
        # Our tolerance depends on how close we are to the object
        agentPos = self.getPosition()
        distanceFromTarget = MathExt.distanceBetweenPoints(agentPos, targetPosition)
        yawRate = self.__getYawRateToFacePosition__(targetPosition)
        pitchRate = self.__getPitchRateToFacePosition__(targetPosition)
        self.__startChangingYaw__(yawRate)
        self.__startChangingPitch__(pitchRate)
        if distanceFromTarget > 7:
            if abs(yawRate) >= .25 or abs(pitchRate) >= .25:
                return False
        else:
            if abs(yawRate) >= .8 or abs(pitchRate) >= .8:
                return False
        return True

    def lookAtEntity(self, entity):
        """
        Begin continuously turning/looking to face the specified entity.
        Returns true if the agent is currently facing the entity. Returns false otherwise.
        """
        # Check action override
        if self.actionOverride != None and self.actionOverride.function != self.lookAtEntity:
            return self.actionOverride.function(*self.actionOverride.args)

        Logger.logLookAtStart(self, entity)
        self.lastStartedLookingAt = entity.id

        # Look at the target
        isLookingAt = self.__lookAtPosition__(entity.position)
        if isLookingAt:
            self.__stopChangingPitch__()
            self.__stopChangingYaw__()
            Logger.logLookAtFinish(self, entity)
            self.lastFinishedLookingAt = entity.id
            return True
        return False

    def lookAtAgent(self, agent):
        """
        Begin continuously turning/looking to face the specified agent.
        Returns true if the agent is currently facing the agent. Returns false otherwise.
        """
        # Check action override
        if self.actionOverride != None and self.actionOverride.function != self.lookAtAgent:
            return self.actionOverride.function(*self.actionOverride.args)

        agentId = agent.getId()
        agentPos = agent.getPosition()
        if agentId == None or agentPos == None:
            return False

        # Represent the agent as an EntityInfo tuple
        agentEntity = EntityInfo(agentId, "agent", agentPos, 1)

        Logger.logLookAtStart(self, agentEntity)
        self.lastStartedLookingAt = agentId

        # Look at the target
        isLookingAt = self.__lookAtPosition__(agentPos)
        if isLookingAt:
            self.__stopChangingPitch__()
            self.__stopChangingYaw__()
            Logger.logLookAtFinish(self, agentEntity)
            self.lastFinishedLookingAt = agentId
            return True
        return False

    def __isAt__(self, targetPosition, tol = 0.5):
        """
        Returns true if this agent is currently at the target position (within the tolerance provided).
        """
        agentPos = self.getPosition()
        if agentPos == None:
            return False

        distance = MathExt.distanceBetweenPointsXZ(agentPos, targetPosition)
        if distance > tol:
            return False
        
        return True

    def __moveToPosition__(self, targetPosition, tol = 0.5, minDistance = 0.0):
        """
        Begin continuously moving to reach a desired Vector position.
        Optionally specify a tolerance, as well as a minimum distance that the agent can be close to the target.
        Returns true if the agent is currently at the desired target. Returns false otherwise.
        """
        agentPos = self.getPosition()
        if agentPos == None:
            return False

        distance = MathExt.distanceBetweenPointsXZ(agentPos, targetPosition)

        if distance < tol and distance > minDistance:
            self.__startMoving__(0.5)   # Slow down movement, expecting caller function to handle completing the stop as necessary
            return True
        elif distance > tol:
            self.__startMoving__(1)
            return False
        else:
            self.__startMoving__(-1)
            return False

    def moveToMob(self, mob):
        """
        Begin continuously moving to reach the specified mob.
        Returns true if the agent is currently within striking distance of the mob. Returns false otherwise.
        """
        # Check action override
        if self.actionOverride != None and self.actionOverride.function != self.moveToMob:
            return self.actionOverride.function(*self.actionOverride.args)

        # Precondition: We are looking at the target
        isLooking = self.__isLookingAt__(mob.position)
        if not isLooking:
            self.stopAllMovement()
            return False

        Logger.logMoveToStart(self, mob)
        self.lastStartedMovingTo = mob.id
        
        # Move to the target
        isAt = self.__moveToPosition__(mob.position, STRIKING_DISTANCE)
        if isAt:
            Logger.logMoveToFinish(self, mob)
            self.lastFinishedMovingTo = mob.id
            self.stopMoving()
            return True
        return False

    def moveToItem(self, item):
        """
        Begin continuously moving to reach a the specified item.
        Returns true if the agent is located at the item. Returns false otherwise.
        """
        # Check action override
        if self.actionOverride != None and self.actionOverride.function != self.moveToItem:
            return self.actionOverride.function(*self.actionOverride.args)

        # Precondition: We are looking at the target
        isLooking = self.__isLookingAt__(item.position)
        if not isLooking:
            self.stopAllMovement()
            return False

        # If this is the first call to move to this item, remember the amount of the item we started with
        if self.lastStartedMovingTo != item.id:
            self.lastItemAmount = self.inventory.amountOfItem(item.type)

        Logger.logMoveToStart(self, item)
        self.lastStartedMovingTo = item.id

        # Move to the target
        isAt = self.__moveToPosition__(item.position, PICK_UP_ITEM_DISTANCE)
        if isAt:
            # Lock this action into repeat and do not officially report true until the item appears in our inventory
            self.actionOverride = Action(self.moveToItem, [item])
            self.inventory.update()
            newAmount = self.inventory.amountOfItem(item.type)
            if newAmount > self.lastItemAmount:
                Logger.logMoveToFinish(self, item)
                self.stopMoving()
                self.lastFinishedMovingTo = item.id
                self.actionOverride = None  # Release lock
                return True
            else:
                return False
        return False

    def moveToBlock(self, block, exact = True):
        """
        Begin continuously moving to reach a specified block. Specify whether the agent should move exactly to the
        block or face it within striking distance. Returns true if the agent has arrived. Returns false otherwise.
        """
        # Check action override
        if self.actionOverride != None and self.actionOverride.function != self.moveToBlock:
            return self.actionOverride.function(*self.actionOverride.args)

        return False

    def moveToAgent(self, agent):
        """
        Begin continuously moving & turning to reach the specified agent.
        Returns true if the agent is currently at the agent. Returns false otherwise.
        """
        # Check action override
        if self.actionOverride != None and self.actionOverride.function != self.moveToAgent:
            return self.actionOverride.function(*self.actionOverride.args)

        agentId = agent.getId()
        agentPos = agent.getPosition()
        if agentPos == None:
            return False
        
        # Represent the agent as an EntityInfo tuple
        agentEntity = EntityInfo(agentId, "agent", agentPos, 1)

        # Precondition: We are looking at target
        isLooking = self.__isLookingAt__(agentPos)
        if not isLooking:
            self.stopAllMovement()
            return False

        Logger.logMoveToStart(self, agentEntity)
        self.lastStartedMovingTo = agentId

        # Move to the target
        isAt = self.__moveToPosition__(agentPos, GIVING_DISTANCE, 2)
        if isAt:
            self.stopMoving()
            Logger.logMoveToFinish(self, agentEntity)
            self.lastFinishedMovingTo = agentId
            return True
        return False

    def craft(self, item, recipeItems):
        """
        Craft an item from other items in this agent's inventory. This requires providing a list of RecipeItems.
        Returns true if the item was successfully crafted and is in the agent's inventory. Returns false otherwise.
        """
        # Check action override
        if self.actionOverride != None and self.actionOverride.function != self.craft:
            return self.actionOverride.function(*self.actionOverride.args)

        # Precondition - We have enough of each recipe item in our inventory
        for recipeItem in recipeItems:
            if self.inventory.amountOfItem(recipeItem.type) < recipeItem.quantity:
                return False

        # Get a list of the items to be used
        itemsUsed = []
        for recipeItem in recipeItems:
            items = self.inventory.allItemsByType(recipeItem.type)
            for i in range(0, recipeItem.quantity):
                itemsUsed.append(items[i])

        # Craft the item and add it to our inventory, recording its id
        self.host.sendCommand("craft {}".format(item.value))
        time.sleep(0.5)

        # Log the successful crafting of the item
        Logger.logCraft(self, item, itemsUsed)
        return True
    
    def attackMob(self, mob):
        """
        Attack a mob using the currently equipped item, provided that it is within striking distance. This method
        calls LookAt if it is necessary for the agent to turn to face the mob. Returns true if successful, and false otherwise.
        """
        # Check action override
        if self.actionOverride != None and self.actionOverride.function != self.attackMob:
            return self.actionOverride.function(*self.actionOverride.args)

        oldMobsKilled = self.getMobsKilled()
        if oldMobsKilled == None:
            return False

        # Precondition: The provided entity is a mob
        if not isMob(mob.type):
            return False

        # Precondition: We are looking at target
        isLooking = self.__isLookingAt__(mob.position)
        if not isLooking:
            self.stopAttacking()
            return False

        # Precondition: We are at the target
        isAt = self.__isAt__(mob.position, STRIKING_DISTANCE)
        if not isAt:
            self.stopAllMovement()
            return False

        self.__startAttacking__()
        self.stopAllMovement()  # Momentarily stop all movement to check if we killed the entity
        time.sleep(0.5)         # Disallows for spamming of the attack action
        newMobsKilled = self.getMobsKilled()

        if newMobsKilled > oldMobsKilled:
            Logger.logAttack(self, mob, True)
        else:
            Logger.logAttack(self, mob, False)

        return True

    def equip(self, item):
        """
        Changes the currently equipped item to something in this agent's inventory. This can cause items to be
        swapped from the hot-bar. Returns true if the specified item is equipped. Returns false otherwise.
        """
        # Check action override
        if self.actionOverride != None and self.actionOverride.function != self.equip:
            return self.actionOverride.function(*self.actionOverride.args)

        # Precondition: We have atleast one of that item
        itemIdx = self.__locationOfItemInInventory__(item)
        if itemIdx == -1:
            return False
        
        # Check if item is already in hotbar (note: key commands are 1-indexed)
        if itemIdx < 9:
            self.host.sendCommand("hotbar.{} 1".format(itemIdx + 1))
            self.host.sendCommand("hotbar.{} 0".format(itemIdx + 1))
            return True
        
        # Try to swap the item into the hotbar where there currently exists no item
        swapIndex = self.__getNextAvailableHotbarIndex__()
        if swapIndex != -1:
            self.host.sendCommand("swapInventoryItems {} {}".format(swapIndex, itemIdx))
            self.host.sendCommand("hotbar.{} 1".format(swapIndex + 1))
            self.host.sendCommand("hotbar.{} 0".format(swapIndex + 1))
            return True

        # Try to swap the item into the index currently in use
        swapIndex = self.getCurrentHotbarIndex()
        if swapIndex != -1:
            self.host.sendCommand("swapInventoryItems {} {}".format(swapIndex, itemIdx))
            self.host.sendCommand("hotbar.{} 1".format(swapIndex + 1))
            self.host.sendCommand("hotbar.{} 0".format(swapIndex + 1))
            return True
        
        return False

    def giveItemToAgent(self, item, agent):
        """
        Give an item in this agent's inventory to another agent.
        Returns true if successful, and false otherwise.
        """
        # Check action override
        if self.actionOverride != None and self.actionOverride.function != self.giveItemToAgent:
            return self.actionOverride.function(*self.actionOverride.args)

        self.stopMoving()  # Make sure we are stopped before checking our direction and position
        agentPos = agent.getPosition()
        if agentPos == None:
            return False

        # Precondition: We have atleast one item of that type
        if self.inventory.amountOfItem(item) == 0:
            return False

        # Precondition: We are at the agent
        isAt = self.__isAt__(agentPos, GIVING_DISTANCE)
        if not isAt:
            return False

        # Remove one item of that type from this agent's inventory
        inventoryItem = self.inventory.itemByType(item)
        if inventoryItem == None:
            return False
        self.inventory.removeItem(inventoryItem)
        agent.inventory.addItem(item.value, inventoryItem.id)   # We must preserve the id of the item

        self.equip(item)
        time.sleep(0.5) # There is a small delay in equipping an item
        self.__throwItem__()
        time.sleep(2)   # Wait for agent to pick up item
        #Logger.logGiveItemToAgent(self, inventoryItem, agent)
        return True
