# ==============================================================================================
# This file contains wrapper classes and functionality relating to a Malmo agent. This combines
# several primitive commands into larger commands that can be used to acheive more complex tasks.
# Logging is also handled automatically for each command that creates a corresponding trace.
# ==============================================================================================
import MalmoPython
import json
import math
from Utils import *


class Agent:
    """
    Wrapper class for a Malmo agent for executing complex commands with corresponding logging.
    To access the Malmo AgentHost object, use the 'host' member.
    """

    def __init__(self):
        self.host = MalmoPython.AgentHost()
        self.mostRecentWorldState = None

    def isMissionActive(self):
        """
        Returns true if this agent's mission is still running.
        """
        return self.host.peekWorldState().is_mission_running

    def getObservations(self):
        """
        Returns the entire world state containing recent observations as a JSON object.
        If no new observations have occurred since the previous call to this method, returns None.
        """
        agentState = self.host.getWorldState()
        if len(agentState.observations) > 0:
            self.mostRecentWorldState = json.loads(agentState.observations[-1].text)
        return self.mostRecentWorldState
        
    def getPosition(self):
        """
        Returns the (x, y, z) position of this agent.
        If no observations have occurred, returns None.
        """
        agentState = self.getObservations()
        if agentState == None:
            return None
        return Vector(agentState["XPos"], agentState["YPos"], agentState["ZPos"])

    def startMoving(self, speed):
        """
        Start moving backwards or forwards at a specific speed. Accepted values range from -1 to 1.
        """
        self.host.sendCommand("move {}".format(speed))

    def stopMoving(self):
        """
        Stop moving forwards/backwards.
        """
        self.host.sendCommand("move 0")

    def startStrafing(self, speed):
        """
        Start moving left or right continuously at a specific speed. Accepted values range from -1 to 1.
        """
        self.host.sendCommand("strafe {}".format(speed))

    def stopStrafing(self, speed):
        """
        Stop moving left/right.
        """
        self.host.sendCommand("strafe 0")

    def startChangingPitch(self, speed):
        """
        Start tilting the agent's head up or down continuously at a specific speed. Accepted values range from -1 to 1.
        """
        self.host.sendCommand("pitch {}".format(speed))

    def stopChangingPitch(self, speed):
        """
        Stop tilting the agent's head up/down.
        """
        self.host.sendCommand("pitch 0")

    def startChangingYaw(self, speed):
        """
        Start turning continuously to the left or right at a specific speed. Accepted values range from -1 to 1.
        """
        self.host.sendCommand("turn {}".format(speed))

    def stopChangingYaw(self):
        """
        Stop turning left/right.
        """
        self.host.sendCommand("turn 0")

    def stopChangingAngle(self):
        """
        Stop any turning left/right and up/down.
        """
        self.stopChangingYaw()
        self.stopChangingPitch()

    def startJumping(self):
        """
        Start jumping continuously.
        """
        self.host.sendCommand("jump 1")

    def stopJumping(self):
        """
        Stop jumping.
        """
        self.host.sendCommand("jump 0")

    def startCrouching(self):
        """
        Start crouching continuously.
        """
        self.host.sendCommand("crouch 1")

    def stopCrouching(self):
        """
        Stop crouching.
        """
        self.host.sendCommand("crouch 0")

    def startAttacking(self):
        """
        Start attacking continuously.
        """
        self.host.sendCommand("attack 1")

    def startUsingItem(self):
        """
        Begin continuously using the item in the currently selected hotbar slot.
        """
        self.host.sendCommand("use 1")

    def stopUsingItem(self):
        """
        Stop using the item in the currently selected hotbar slot.
        """
        self.host.sendCommand("use 0")

    def getNearestMobPosition(self, mobType):
        """
        Returns the EntityInfo of the nearest mob of a specific type within a 10x10 area around this agent.
        Returns None if no mob of that type is within the area.
        """
        worldState = self.getObservations()
        if worldState == None:
            return None
        agentPos = Vector(worldState["XPos"], worldState["YPos"], worldState["ZPos"])
        entities = [EntityInfo(Vector(k["x"], k["y"], k["z"]), k["name"], k.get("quantity")) for k in worldState["nearby_entities"]]
        nearestDistance = 1000000
        nearestEntity = None
        for entity in entities:
            if entity.name == mobType.value:
                entityPos = entity.position
                distanceToPig = MathExt.distanceBetweenPoints(agentPos, entityPos)
                if distanceToPig < nearestDistance:
                    nearestDistance = distanceToPig
                    nearestEntity = entity
        if nearestEntity == None:
            return None
        return nearestEntity

    def __changeYawAngleToFacePosition__(self, targetPosition):
        """
        Begin continuously turning to face a position relative to the agent's current position.
        If unable to determine the agent's current position, does nothing.
        """
        worldState = self.getObservations()
        if worldState == None:
            return
        agentPos = Vector(worldState["XPos"], worldState["YPos"], worldState["ZPos"])
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
        self.startChangingYaw(rate)

    def __changePitchAngleToFacePosition__(self, targetPosition):
        """
        Begin continuously changing pitch of this agent to face a particular (x,y,z) position.
        If unable to determine the agent's current position, does nothing.
        """
        worldState = self.getObservations()
        if worldState == None:
            return
        agentPos = Vector(worldState["XPos"], worldState["YPos"] + 1, worldState["ZPos"])     # Agent's head is above the agent's location
        currentAngle = worldState["Pitch"]
        vectorWithHeight = MathExt.vectorFromPoints(agentPos, targetPosition)
        vectorWithHeight = MathExt.normalizeVector(vectorWithHeight)
        vectorWithoutHeight = Vector(vectorWithHeight.x, 0, vectorWithHeight.z)

        # Get the angle that we wish to change the pitch to (account for range -90 to 90)
        if MathExt.isZeroVector(vectorWithHeight) or MathExt.isZeroVector(vectorWithoutHeight): # Avoid dividing by 0
            return
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

        self.startChangingPitch(rate)        

    def lookAt(self, targetPosition):
        """
        Begin continuously turning/looking to face an (x,y,z) position.
        If unable to determine the agent's current position, does nothing.
        """
        self.__changeYawAngleToFacePosition__(targetPosition)
        self.__changePitchAngleToFacePosition__(targetPosition)