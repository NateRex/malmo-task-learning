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
        self.playersKilled = 0 # Do
        self.currentHealth = 20.0
        self.healthLost = 0.0
        self.isAlive = True # Do
        self.timeAlive = 0.0 # Do
        self.food = 0.0 # Do
        self.score = 0.0 # Do
        self.xp = 0.0 # Do
        self.distanceTravelled = 0.0 # Do


    def checkHealth(self, agent):
        """
        Checks if the agent has lost health and if so, adds to the healthLost stat. If health is gained, currentHealth is adjusted.
        If health reaches 0, agent is dead and isDead is changed to true.
        Should be checked frequently throughout an Agent's mission.
        """
        health = agent.getCurrentHealth()
        if health == None:
            return
        if(health < self.currentHealth):
            self.healthLost += self.currentHealth - health
        if(health == 0.0):
            self.isAlive = False
        self.currentHealth = health

    def logStats(self, agent):
        """
        Logs the damageDealt, mobsKilled, playersKilled, timeAlive, food, score, xp, and distanceTravelled stats for a specific agent.
        Should be checked at the very end of a mission.
        """
        self.damageDealt = agent.getDamageDealt()
        self.mobsKilled = agent.getMobsKilled()
        self.playersKilled = agent.getPlayersKilled()
        self.timeAlive = agent.getTimeAlive()
        self.food = agent.getCurrentFoodState()
        self.score = agent.getCurrentScore()
        self.xp = agent.getCurrentXP()
        self.distanceTravelled = agent.getCurrentDistanceTravelled()


    def printStats(self, agent):
        """
        Prints out all of the agent's stat information recorded throughout the mission.
        """
        fileName = datetime.fromtimestamp(time.time()).strftime('%m_%d_%Y_%H_%M_%S') + ".txt"
        filePath = "stats"
        if not os.path.isdir(filePath):
            os.mkdir(filePath)
        filePath = os.path.join(filePath, fileName)
        statFile = open(filePath, "w+")
        statFile.write(agent.getId() + "\n")
        statFile.write("-------------------\n")
        statFile.write("Damage Dealt: " + str(self.damageDealt) +"\n")
        statFile.write("EnemiesKilled: " + str(self.mobsKilled) +"\n")
        statFile.write("PlayersKilled: " + str(self.playersKilled) + "\n")
        statFile.write("CurrentHealth: " + str(self.currentHealth) + "\n")
        statFile.write("Health Lost: " + str(self.healthLost) + "\n")
        statFile.write("Is Alive: " + str(self.isAlive) + "\n")
        statFile.write("Time Alive: " + str(self.timeAlive) + "\n")
        statFile.write("Food: " + str(self.food) + "\n")
        statFile.write("Score: " + str(self.score) + "\n")
        statFile.write("XP: " + str(self.xp) + "\n")
        statFile.write("DistanceTravelled: " + str(self.distanceTravelled) + "\n")
        statFile.close()
        print("Mission stats output has been saved to: " + filePath)
