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
        super.__init__(name)