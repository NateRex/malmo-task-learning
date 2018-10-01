# ==============================================================================================
# This file contains wrapper classes and functionality relating to a Malmo agent. This combines
# several primitive commands into larger commands that can be used to acheive more complex tasks.
# Logging is also handled automatically for each command that creates a corresponding trace.
# ==============================================================================================
import MalmoPython
import json

class Agent:
    """
    Wrapper class for a Malmo agent for executing complex commands with corresponding logging.
    To access the Malmo AgentHost object, use the 'host' member.
    """

    def __init__(self):
        self.host = MalmoPython.AgentHost()

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
        if worldState.number_of_observations_since_last_state > 0:
            return json.loads(worldState.observations[-1].text)
        return None
        

    def move(self, speed):
        """
        Start moving backwards or forwards at a specific speed. Accepted values range from -1 to 1.
        A speed of 0 stops the agent.
        """
        self.host.sendCommand("move {}".format(speed))

    def strafe(self, speed):
        """
        Start moving left or right at a specific speed. Accepted values range from -1 to 1.
        A speed of 0 stops the agent.
        """
        self.host.sendCommand("strafe {}".format(speed))

    def look(self, speed):
        """
        Start tilting the agent's head up or down at a specific speed. Accepted values range from -1 to 1.
        A speed of 0 stops the agent.
        """
        self.host.sendCommand("pitch {}".format(speed))

    def turn(self, speed):
        """
        Start turning to the left or right at a specific speed. Accepted values range from -1 to 1.
        A speed of 0 stops the agent.
        """
        self.host.sendCommand("turn {}".format(speed))

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