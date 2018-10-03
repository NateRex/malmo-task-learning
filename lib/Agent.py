# ==============================================================================================
# This file contains wrapper classes and functionality relating to a Malmo agent. This combines
# several primitive commands into larger commands that can be used to acheive more complex tasks.
# Logging is also handled automatically for each command that creates a corresponding trace.
# ==============================================================================================
import MalmoPython
import json
import math
from collections import namedtuple
from Utils import MathExt

EntityInfo = namedtuple('EntityInfo', 'x, y, z, name, quantity')

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
        Returns the world state containing all recent observations as a JSON object.
        If no new observations have occurred since the previous call to this method, returns None.
        """
        worldState = self.host.getWorldState()
        if len(worldState.observations) > 0:
            self.mostRecentWorldState = json.loads(worldState.observations[-1].text)
        return self.mostRecentWorldState
        

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

    def startTurning(self, speed):
        """
        Start turning continuously to the left or right at a specific speed. Accepted values range from -1 to 1.
        """
        self.host.sendCommand("turn {}".format(speed))

    def stopTurning(self):
        """
        Stop turning left/right.
        """
        self.host.sendCommand("turn 0")

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
        Returns the position of the nearest mob of a specific type within a 10x10 area around this agent.
        Returns None if no mob of that type is within the area.
        """
        worldState = self.getObservations()
        if worldState == None:
            return None
        agentPos = (worldState["XPos"], worldState["YPos"], worldState["ZPos"])
        entities = [EntityInfo(k["x"], k["y"], k["z"], k["name"], k.get("quantity")) for k in worldState["nearby_entities"]]
        nearestDistance = 1000000
        nearestPosition = None
        for entity in entities:
            if entity.name == mobType.value:
                entityPos = (entity.x, entity.y, entity.z)
                distanceToPig = MathExt.distanceBetweenPoints(agentPos, entityPos)
                if distanceToPig < nearestDistance:
                    nearestDistance = distanceToPig
                    nearestPosition = entityPos
        if nearestPosition == None:
            return None
        return nearestPosition

    def __turningRateFromAngleDifference__(self, currentAngle, targetAngle):
        """
        Internal method for calculating how fast to turn or change pitch based on a difference
        of angles.
        """
        diff = None
        multiplier = 1
        if currentAngle <= targetAngle:
            diff = targetAngle - currentAngle
        else:
            diff = currentAngle - targetAngle
            multiplier = -1
        
        if diff > 10:
            return 1.0 * multiplier
        elif diff > 5:
            return .25 * multiplier
        return MathExt.affineTransformation(diff, 0.0, 180.0, 0, 1.0) * multiplier


    def turnToPosition(self, targetPosition):
        """
        Begin continuously turning to face a position relative to the agent's current position.
        If unable to determine the agent's current position, does nothing.
        """
        worldState = self.getObservations()
        if worldState == None:
            return
        agentPos = (worldState["XPos"], worldState["YPos"], worldState["ZPos"])
        currentYaw = worldState["Yaw"] if worldState["Yaw"] >= 0 else 360.0 - worldState["Yaw"]
        vector = MathExt.vectorFromPoints(agentPos, targetPosition)
        vector = MathExt.normalizeVector(vector)

        newYaw = None
        if MathExt.valuesAreEqual(vector[0], 0, 1.0e-14): # Avoid dividing by 0
            if vector[2] >= 0:
                newYaw = -MathExt.PI_OVER_TWO
            else:
                newYaw = MathExt.PI_OVER_TWO
        else:
            newYaw = math.atan(vector[2] / vector[0])
    
        # Adjust angle based on quadrant of vector
        if vector[0] <= 0:   # Quadrant 1 or 2
            newYaw = MathExt.PI_OVER_TWO + newYaw
        elif vector[0] > 0:  # Quadrant 3 or 4
            newYaw = MathExt.THREE_PI_OVER_TWO + newYaw

        newYaw = math.degrees(newYaw)
        if MathExt.valuesAreEqual(newYaw, 360.0, 1.0e-14):
            newYaw = 0

        self.startTurning(self.__turningRateFromAngleDifference__(currentYaw, newYaw))

        