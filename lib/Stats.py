# ==============================================================================================
# This file contains methods used to record statistics on the various agents running as they perform
# in a given scenario.
# ==============================================================================================
import MalmoPython
import json
import math
import time
from Utils import *
from Logger import *
from Constants import *
from AgentInventory import *
from Agent import *

class Stats:
    """
    This file contains methods used to record statistics on the various agents running as they perform
    in a given scenario.
    """

    def __init__(self):
        self.damageDealt = 0
        self.mobsKilled = 0
        self.currentHealth = 20.0
        self.healthLost = 0.0

    def checkHealth(self, agent):
        health = agent.getCurrentHealth()
        if(health < self.currentHealth):
            self.healthLost = self.currentHealth - health
        self.currentHealth = health

    def logStats(self, agent):
        self.damageDealt = agent.getDamageDealt()
        self.mobsKilled = agent.getMobsKilled()

    def printStats(self, agent):
        print(agent.getId())
        print("______________________")
        print("Damage Dealt: ", self.damageDealt)
        print("EnemiesKilled: ", self.mobsKilled)
        print("Health Lost: ", self.healthLost)
        print()