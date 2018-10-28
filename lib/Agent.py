# ==============================================================================================
# This file contains wrapper classes and functionality relating to a Malmo agent. This combines
# several primitive commands into larger commands that can be used to acheive more complex tasks.
# Logging is also handled automatically for each command that creates a corresponding trace.
# ==============================================================================================
import MalmoPython
import json
import math
from Utils import *
from Logger import *
from Constants import *


class Agent:
    """
    Wrapper class for a Malmo agent for executing complex commands with corresponding logging.
    To access the Malmo AgentHost object, use the 'host' member.
    """

    def __init__(self):
        self.host = MalmoPython.AgentHost()
        self.lastWorldState = None
        self.lastMovedTo = None     # Id of the entity we last moved to

    def isMissionActive(self):
        """
        Returns true if this agent's mission is still running.
        """
        return self.host.peekWorldState().is_mission_running

    def getObservations(self):
        """
        Returns the entire world state containing the most recent observations as a JSON object.
        If no new observations have occurred since the previous call to this method, returns None.
        """
        agentState = self.host.getWorldState()
        if len(agentState.observations) > 0:
            self.lastWorldState = json.loads(agentState.observations[-1].text)
        return self.lastWorldState

    def getId(self):
        """
        Returns the unique identifier for this agent. Returns none if unsuccessful.
        """
        agentState = self.getObservations()
        if agentState == None:
            return None
        return "{}{}".format(agentState["Name"], agentState["nearby_entities"][0]["id"]).replace("-", "")  # Agent itself is always the first entity closeby

    def getPosition(self):
        """
        Returns the Vector position of this agent.
        If no observations have occurred, returns None.
        """
        agentState = self.getObservations()
        if agentState == None:
            return None
        return Vector(agentState["XPos"], agentState["YPos"] + 1, agentState["ZPos"])   # Agent's head is above the agent's location

    def getInventory(self):
        """
        Returns an array of inventory items that this agent is currently carrying.
        If no observations have occurred, returns None.
        """
        agentState = self.getObservations()
        if agentState == None:
            return None
        return agentState["inventory"]

    def getCurrentHotbarIndex(self):
        """
        Returns the hotbar index (0-based) that this agent currently has selected.
        If unable to determine the currently used hotbar index, returns -1.
        """
        agentState = self.getObservations()
        if agentState == None:
            return -1
        return agentState["currentItemIndex"]

    def __getNextAvailableHotbarIndex__(self):
        """
        Internal method that returns the next hotbar index (0-based) that is empty.
        If there is no such slot available, returns -1.
        """
        inventory = self.getInventory()
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
        inventory = self.getInventory()
        if inventory == None:
            return -1
        
        for i in range(0, len(inventory)):
            currentItem = inventory[i]
            if currentItem["type"] == item.value:
                return currentItem["index"] 
        return -1

    def amountOfItemInInventory(self, item):
        """
        Returns the quantity of a particular item in this agent's inventory. Returns 0 on error.
        """
        inventory = self.getInventory()
        if inventory == None:
            return 0
        
        numberFound = 0
        for i in range(0, len(inventory)):
            currentItem = inventory[i]
            if currentItem["type"] == item.value:
                numberFound += currentItem["quantity"]
        return numberFound

    def __startMoving__(self, speed):
        """
        Start moving backwards or forwards at a specific speed. Accepted values range from -1 to 1.
        """
        self.host.sendCommand("move {}".format(speed))

    def __stopMoving__(self):
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
        self.__stopChangingYaw__()
        self.__stopChangingPitch__()
        self.__stopMoving__()

    def getNearbyEntities(self):
        """
        Returns a list of named EntityInfo tuples of all entities within a 20x20 area around this agent.
        Returns None on error.
        """
        worldState = self.getObservations()
        if worldState == None:
            return None
        entities = [EntityInfo("{}{}".format(k["name"], k["id"]).replace("-", ""), k["name"], Vector(k["x"], k["y"], k["z"]), k.get("quantity")) for k in worldState["nearby_entities"]]
        return entities

    def getClosestEntityByType(self, entityType):
        """
        Returns a named EntityInfo tuple of the nearest entity of a specific type within a 20x20 area around this agent.
        Returns None if no entity of that type is within the area.
        """
        agentPos = self.getPosition()
        entities = self.getNearbyEntities()
        if agentPos == None or entities == None:
            return None
        nearestDistance = 1000000
        nearestEntity = None
        for entity in entities:
            if entity.type == entityType.value:
                entityPos = entity.position
                distanceToPig = MathExt.distanceBetweenPoints(agentPos, entityPos)
                if distanceToPig < nearestDistance:
                    nearestDistance = distanceToPig
                    nearestEntity = entity
        if nearestEntity == None:
            return None
        Logger.logClosestEntity(self, nearestEntity)
        return nearestEntity

    def __changeYawAngleToFacePosition__(self, targetPosition):
        """
        Begin continuously turning to face a Vector position relative to the agent's current position.
        Returns true if the agent is currently facing the target. Returns false otherwise.
        """
        worldState = self.getObservations()
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

        self.__startChangingYaw__(rate)
        if rate < 0.1:
            return True
        else:
            return False

    def __changePitchAngleToFacePosition__(self, targetPosition):
        """
        Begin continuously changing pitch of this agent to face a particular Vector position.
        Returns true if the agent is currently facing the target. Returns false otherwise.
        """
        worldState = self.getObservations()
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

        self.__startChangingPitch__(rate)
        if rate < 0.1:
            return True
        else:
            return False

    def lookAtPosition(self, targetPosition):
        """
        Begin continuously turning/looking to face a Vector position.
        Returns true if the agent is currently looking at the target. Returns false otherwise.
        """
        return self.__changeYawAngleToFacePosition__(targetPosition) and self.__changePitchAngleToFacePosition__(targetPosition)

    def __moveToPosition__(self, targetPosition):
        """
        Begin continuously moving & turning to reach a desired Vector position (within 2-3 blocks).
        Returns true if the agent is currently facing and at the desired target. Returns false otherwise.
        """
        agentPos = self.getPosition()
        if agentPos == None:
            return False  
        
        isLookingAtTarget = self.lookAtPosition(targetPosition)
        if not isLookingAtTarget:
            self.__stopMoving__()
            return False

        distance = MathExt.distanceBetweenPoints(agentPos, targetPosition)

        if distance < 2.8:     # Already at the desired location (just make sure we are facing correct way)
            self.__stopMoving__()
            return True
        else:
            self.__startMoving__(1)
            return False

    def moveTo(self, entity):
        """
        Begin continuously moving & turning to reach a desired entity that was found from observations.
        Returns true if the agent is currently facing and at the specified entity. Returns false otherwise.
        """
        Logger.logMoveToStart(self, entity)
        if self.__moveToPosition__(entity.position):
            Logger.logMoveToFinish(self, entity)
            self.lastMovedTo = entity.id
            return True
        return False

    def craft(self, item, recipe):
        """
        Craft an item using the ingredients list of RecipeItems given.
        Returns true if the item was successfully crafted and is in the agent's inventory. Returns false otherwise.
        """
        initialAmt = self.amountOfItemInInventory(item)
        self.host.sendCommand("craft {}".format(item))
        newAmt = self.amountOfItemInInventory(item)
        if (newAmt > initialAmt):
            Logger.logCraft(self, LoggableCommand(AgentCommands.Craft, CraftArgs(item, recipe)))
            return True
        else:
            return False
    
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