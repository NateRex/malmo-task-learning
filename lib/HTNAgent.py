# ==============================================================================================
# This file contains code for the HTNAgent class, representing an Agent that interfaces with
# a trained HTN in order to select actions based on the current environment state.
# ==============================================================================================
from Agent import *

class HTNAgent(Agent):
    """
    Wrapper class for a Malmo agent that interfaces with a trained hierarchical task network
    in order to select actions based on the current state.
    """

    def __init__(self, name):
        super(HTNAgent, self).__init__(name)

    def __selectAction__(self, actionStr):
        """
        Given an action to perform as a string with parameters, select the appropriate agent action to perform and return it
        along with any parameters in a tuple object.
        """
        if actionStr.startswith("!LOOKAT"):
            # There are several versions of the lookAt command, depending on the entity
            ### TODO
