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
from Constants import *
from AgentInventory import *
from Stats import *


class Agent:
    """
    Wrapper class for a Malmo agent for executing complex commands with corresponding logging.
    To access the Malmo AgentHost object, use the 'host' member.
    """
    
    def __init__(self):
        self.host = MalmoPython.AgentHost()
        self.inventory = AgentInventory()
        self.lastWorldState = None
        self.lastLookedAt = None    # Id of the entity we last looked at
        self.lastMovedTo = None     # Id of the entity we last moved to
        self.stats = Stats()

    def isMissionActive(self):
        """
        Returns true if this agent's mission is still running.
        """
        return self.host.peekWorldState().is_mission_running

    def getObservation(self):
        """
        Returns the entire world state containing the most recent observations as a JSON object.
        """
        agentState = self.host.getWorldState()
        if len(agentState.observations) > 0:
            self.lastWorldState = json.loads(agentState.observations[-1].text)
        return self.lastWorldState

    def waitForNextObservation(self):
        """
        Waits for the observations of this agent to change.
        """
        agentState = self.host.getWorldState()
        observationsPassed = agentState.number_of_observations_since_last_state
        while observationsPassed <= 0:
            agentState = self.host.getWorldState()
            observationsPassed = agentState.number_of_observations_since_last_state
        self.lastWorldState = json.loads(agentState.observations[-1].text)
        return

    def getId(self):
        """
        Returns the unique identifier for this agent. Returns none if unsuccessful.
        """
        agentState = self.getObservation()
        if agentState == None:
            return None
        return agentState["Name"]

    def getPosition(self):
        """
        Returns the Vector position of this agent.
        If no observations have occurred, returns None.
        """
        agentState = self.getObservation()
        if agentState == None:
            return None
        return Vector(agentState["XPos"], agentState["YPos"] + 1, agentState["ZPos"])   # Agent's head is above the agent's location

    def getDamageDealt(self):
        """
        Returns the amount of damage this agent has dealt out to other entities.
        If no observations have occurred, returns None.
        """
        agentState = self.getObservation()
        if agentState == None:
            return None
        return agentState["DamageDealt"]

    def getMobsKilled(self):
        """
        Returns the number of mobs this agent has killed.
        If no observations have occurred, returns None.
        """
        agentState = self.getObservation()
        if agentState == None:
            return None
        return agentState["MobsKilled"]

    def getPlayersKilled(self):
        """
        Returns the number of players this agent has killed.
        If no observations have occured, returns None.
        """
        agentState = self.getObservation()
        if agentState == None:
            return None
        return agentState["PlayersKilled"]

    def getTimeAlive(self):
        """
        Returns the time the agent has been alive for
        If no observations have occured, returns None.
        """
        agentState = self.getObservation()
        if agentState == None:
            return None
        return agentState["TimeAlive"]

    def getCurrentFoodState(self):
        """
        Returns the hunger level of the agent.
        If no observations have occured, returns None.
        """
        agentState = self.getObservation()
        if agentState == None:
            return None
        return agentState["Food"]

    def getCurrentScore(self):
        """
        Returns the score of the agent.
        If no observations have occured, returns None.
        """
        agentState = self.getObservation()
        if agentState == None:
            return None
        return agentState["Score"]

    def getCurrentXP(self):
        """
        Returns the xp of the agent.
        If no observations have occured, returns None.
        """
        agentState = self.getObservation()
        if agentState == None:
            return None
        return agentState["XP"]

    def getCurrentDistanceTravelled(self):
        """
        Returns the distance travelled by the agent.
        If no observations have occured, returns None.
        """
        agentState = self.getObservation()
        if agentState == None:
            return None
        return agentState["DistanceTravelled"]

    def getCurrentHealth(self):
        """
        Returns the current health of the agent.
        """
        agentState = self.getObservation()
        if agentState == None:
            return None
        return agentState["Life"]

    def getCurrentHunger(self):
        """
        Returns the current hunger of the agent.
        """
        agentState = self.getObservation()
        if agentState == None:
            return None
        return agentState[u'Hunger']

    def getInventoryJson(self):
        """
        Returns an array of JSON inventory items that this agent is currently carrying.
        If no observations have occurred, returns None.
        """
        agentState = self.getObservation()
        if agentState == None:
            return None
        return agentState["inventory"]

    def getCurrentHotbarIndex(self):
        """
        Returns the hotbar index (0-based) that this agent currently has selected.
        If unable to determine the currently used hotbar index, returns -1.
        """
        agentState = self.getObservation()
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
        worldState = self.getObservation()
        if worldState == None:
            return None
        entities = [EntityInfo("{}{}".format(k["name"], k["id"]).replace("-", ""), k["name"], Vector(k["x"], k["y"], k["z"]), k.get("quantity")) for k in worldState["nearby_entities"]]
        return entities

    def getClosestEntity(self):
        """
        Returns a named EntityInfo tuple of the nearest entity within a 20x20 area of this agent.
        Returns none if no such entity exists.
        """
        agentPos = self.getPosition()
        entities = self.getNearbyEntities()
        if agentPos == None or entities == None:
            return None
        nearestDistance = 1000000
        nearestEntity = None
        for i in range(1, len(entities)):   # First entity is always the agent itself
            entity = entities[i]
            entityPos = entity.position
            distanceToEntity = MathExt.distanceBetweenPoints(agentPos, entityPos)
            if distanceToEntity < nearestDistance:
                nearestDistance = distanceToEntity
                nearestEntity = entity
        if nearestEntity == None:
            return None
        Logger.logClosestEntity(self, entity)

    def getClosestPeacefulEntity(self):
        """
        Returns a named EntityInfo tuple of the nearest peaceful entity within a 20x20 area of this agent.
        Returns None if no such entity exists.
        """
        agentPos = self.getPosition()
        entities = self.getNearbyEntities()
        if agentPos == None or entities == None:
            return None
        nearestDistance = 1000000
        nearestEntity = None
        for entity in entities:
            if entity.type in MobType.Peaceful.__members__:
                entityPos = entity.position
                distanceToEntity = MathExt.distanceBetweenPoints(agentPos, entityPos)
                if distanceToEntity < nearestDistance:
                    nearestDistance = distanceToEntity
                    nearestEntity = entity
        if nearestEntity == None:
            return None
        Logger.logClosestPeacefulEntity(self, entity)
        return nearestEntity

    def getClosestHarmfulEntity(self):
        """
        Returns a named EntityInfo tuple of the nearest harmful entity within a 20x20 area of this agent.
        Returns None if no such entity exists.
        """
        agentPos = self.getPosition()
        entities = self.getNearbyEntities()
        if agentPos == None or entities == None:
            return None
        nearestDistance = 1000000
        nearestEntity = None
        for entity in entities:
            if entity.type in MobType.Hostile.__members__:
                entityPos = entity.position
                distanceToEntity = MathExt.distanceBetweenPoints(agentPos, entityPos)
                if distanceToEntity < nearestDistance:
                    nearestDistance = distanceToEntity
                    nearestEntity = entity
        if nearestEntity == None:
            return None
        Logger.logClosestHarmfulEntity(self, entity)
        return nearestEntity

    def getClosestBlockLocation(self, blockType):
        """
        Returns the  nearest block of a given type as an entity.
        """
        agentState = self.getObservation()
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
        worldState = self.getObservation()
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
        else:
            rate = MathExt.affineTransformation(diff, 0.0, 180.0, 0, 1.0) * multiplier

        return rate

    def __getPitchRateToFacePosition__(self, targetPosition):
        """
        Obtain a rate in which to turn along the pitch angle to face the given target position.
        """
        worldState = self.getObservation()
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
        else:
            rate = MathExt.affineTransformation(diff, 0.0, 180.0, 0, 1.0) * multiplier

        return rate

    def __isLookingAt__(self, targetPosition):
        """
        Returns true if this agent is currently looking in the proximity of the target position.
        """
        yawRate = self.__getYawRateToFacePosition__(targetPosition)
        if abs(yawRate) > .25:
            return False
        pitchRate = self.__getPitchRateToFacePosition__(targetPosition)
        if abs(pitchRate) > .25:
            return False
        return True

    def __lookAtPosition__(self, targetPosition):
        """
        Begin continuously turning/looking to face a Vector position.
        Returns true if the agent is currently looking at the target. Returns false otherwise.
        """
        yawRate = self.__getYawRateToFacePosition__(targetPosition)
        pitchRate = self.__getPitchRateToFacePosition__(targetPosition)
        self.__startChangingYaw__(yawRate)
        self.__startChangingPitch__(pitchRate)
        return abs(yawRate) <= .25 and abs(pitchRate) <= .25

    def lookAt(self, entity):
        """
        Begin continuously turning/looking to face the specified entity.
        Returns true if the agent is currently facing the entity. Returns false otherwise.
        """
        Logger.logLookAtStart(self, entity)
        isLookingAt = self.__lookAtPosition__(entity.position)
        if isLookingAt:
            Logger.logLookAtFinish(self, entity)
            self.lastLookedAt = entity.id
            return True
        return False

    def __moveToPosition__(self, targetPosition):
        """
        Begin continuously moving & turning to reach a desired Vector position (within 2-3 blocks).
        Returns true if the agent is currently facing and at the desired target. Returns false otherwise.
        """
        agentPos = self.getPosition()
        if agentPos == None:
            return False  

        distance = MathExt.distanceBetweenPoints(agentPos, targetPosition)

        if distance <= STRIKING_DISTANCE:  # Moving "to" a position is really moving "up to it" while facing it
            self.stopMoving()
            return True
        else:
            self.__startMoving__(1)
            return False

    def moveTo(self, entity):
        """
        Begin continuously moving & turning to reach a desired entity that was found from observations.
        Returns true if the agent is currently facing and at the specified entity. Returns false otherwise.
        """
        # Precondition: We are looking at target
        isLooking = self.__isLookingAt__(entity.position)
        if not isLooking:
            self.stopMoving()
            return False

        Logger.logMoveToStart(self, entity)
        
        # Move to the target
        isAt = self.__moveToPosition__(entity.position)
        if isAt:
            Logger.logMoveToFinish(self, entity)
            self.lastMovedTo = entity.id
            return True
        return False

    def craft(self, item, recipeItems):
        """
        Craft an item from other items in this agent's inventory. This requires providing a list of RecipeItems.
        Returns true if the item was successfully crafted and is in the agent's inventory. Returns false otherwise.
        """
        inventoryJson = self.getInventoryJson()
        if inventoryJson == None:
            return False
        self.inventory.update(inventoryJson) # update the inventory in case we picked up any new items by chance

        # Precondition - We have enough of each recipe item in our inventory
        for recipeItem in recipeItems:
            if self.inventory.amountOfItem(recipeItem.type) < recipeItem.quantity:
                return False

        # Get a list of the items to be used
        itemsUsed = []
        for recipeItem in recipeItems:
            items = self.inventory.getItemsByType(recipeItem.type)
            for i in range(0, recipeItem.quantity):
                itemsUsed.append(items[i])

        # Craft the item and add it to our inventory, recording its id
        self.host.sendCommand("craft {}".format(item.value))
        itemCrafted = self.inventory.addItem(item)

        # Remove the items used from the inventory
        for itemUsed in itemsUsed:
            self.inventory.removeItem(itemUsed)

        # Log the successful crafting of the item
        Logger.logCraft(self, itemCrafted, itemsUsed)
        return True
    
    def attack(self, entity):
        """
        Attack an entity using the currently equipped item, provided that it is within striking distance. This method
        calls LookAt if it is necessary for the agent to turn to face the entity.
        """
        agentPos = self.getPosition()
        oldMobsKilled = self.getMobsKilled()
        if agentPos == None or oldMobsKilled == None:
            return False

        # Precondition: We are looking at target
        isLooking = self.__isLookingAt__(entity.position)
        if not isLooking:
            self.stopAttacking()
            return False

        # Precondition: We are at the target
        distance = MathExt.distanceBetweenPoints(agentPos, entity.position)
        if distance > STRIKING_DISTANCE:
            self.stopAttacking()
            return False

        self.__startAttacking__()
        self.stopAllMovement()  # Momentarily stop everything to check if we killed the entity
        time.sleep(0.6)
        newMobsKilled = self.getMobsKilled()

        if newMobsKilled > oldMobsKilled:
            Logger.logAttack(self, entity, True)
        else:
            Logger.logAttack(self, entity, False)

        return True

    def equip(self, item):
        """
        Changes the currently equipped item to something in this agent's inventory. This can cause items to be
        swapped from the hot-bar. Returns true if the specified item is equipped. Returns false otherwise.
        """
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








    def moveToPlayer(self, player):
        """
        Begin continuously moving & turning to reach a desired entity that was found from observations.
        Returns true if the agent is currently facing and at the specified entity. Returns false otherwise.
        """
        #Logger.logMoveToStart(self, player)

        # Look at the target
        isLookingAtTarget = self.lookAtPlayer(player)
        if not isLookingAtTarget:
            self.stopMoving()
            return False
        
        # Move to the target
        if self.__moveToPosition__(player):
            #Logger.logMoveToFinish(self, player)
            #self.lastMovedTo = player.id
            return True
        return False

    def lookAtPlayer(self, player):
        """
        Begin continuously turning/looking to face the specified entity.
        Returns true if the agent is currently facing the entity. Returns false otherwise.
        """
        #Logger.logLookAtStart(self, player)
        isLookingAt = self.__lookAtPosition__(player)
        if isLookingAt:
            #Logger.logLookAtFinish(self, player)
            #self.lastLookedAt = player.id
            return True
        return False

    def __throwItem__(self):
        """
        Throws item in hand forward
        """
        self.host.sendCommand("discardCurrentItem")

    def __placeItemAt__(self, location):
        """
        Places an item at a location in the hotbar.
        Returns true if successful
        """
        itemIdx = self.__locationOfItemInInventory__(item)
        if itemIdx == -1:
            return False
        if location < 9 and location >= 0:
            self.host.sendCommand("swapInventoryItems {} {}".format(location, itemIdx))
            #self.host.sendCommand("hotbar.{} 1".format(swapIndex + 1))
            #self.host.sendCommand("hotbar.{} 0".format(swapIndex + 1))
            return True

    def giveItem(self, item):
        """
        Give an item to a player that is in inventory.
        Returns none if the item wasn't in inventory.
        """
        if self.amountOfItemInInventory(item) > 0:
            self.equip(item)
            if self.__locationOfItemInInventory__(item) == self.getCurrentHotbarIndex():
                self.__throwItem__()
        else:
            return None
