# ==============================================================================================
# This file contains methods used to record statistics on agents as they perform
# in a mission scenario.
# ==============================================================================================
import MalmoPython
import json
import math
import time
import pandas
import matplotlib.pyplot as plt
import sys
import random
from Utils import *
from Logger import *

# A tuple containing agent IDs paired with dataframes containing the stats of that agent from a mission
AgentData = namedtuple("AgentData", "agent_id data")
# A list of all of the attribute names we track
attribute_names = ["SysTime", "DamageDealt", "MobsKilled", "PlayersKilled", "CurrentHealth", "HealthLost", "IsAlive", "TimeAlive", "Hunger", "Score", "XP", "DistanceTravelled"]

# ===========================================================================================================
# Classes
# ===========================================================================================================

class Stats:
    """
    This file contains methods used to record statistics on the various agents running as they perform
    in a given scenario.
    """
    startTime = time.time()

    def __init__(self, agent):
        self.agent = agent              # Although an object of this class is a member of the Agent class, store a reference to the agent
        self.updateCounter = 100        # A counter to track when to actually conduct an update
        self.currentHealth = 20.0       # Current health
        self.healthLost = 0.0           # Total amount of health lost
        self.isAlive = True             # Whether or not the agent is alive

        # A pandas dataframe storing all of the data over time in CSV format
        self.data = pandas.DataFrame(columns=attribute_names)
        self.dataIdx = 0

    def __updateHealth__(self):
        """
        Checks if the agent has lost health and if so, adds to the healthLost stat. If health is gained, currentHealth is adjusted.
        If health reaches 0, agent is dead and isDead is changed to true.
        Should be checked frequently throughout an Agent's mission.
        """
        health = self.agent.getHealth()
        if health == None:
            return
        if health < self.currentHealth:
            self.healthLost += self.currentHealth - health
        if health == 0.0:
            self.isAlive = False
        self.currentHealth = health

    def update(self):
        """
        Logs the damageDealt, mobsKilled, playersKilled, timeAlive, hunger, score, xp, and distanceTravelled stats for a specific agent.
        Should be checked at the very end of a mission.
        """
        if self.updateCounter == 100:
            self.__updateHealth__()
            self.data.loc[self.dataIdx] = [time.time() - Stats.startTime, self.agent.getDamageDealt(), self.agent.getMobsKilled(), self.agent.getPlayersKilled(), self.currentHealth, self.healthLost, self.isAlive, self.agent.getTimeAlive(), self.agent.getHunger(), self.agent.getScore(), self.agent.getXP(), self.agent.getDistanceTravelled()]
            self.updateCounter = 0
            self.dataIdx += 1
        else:
            self.updateCounter += 1

    def export(self):
        """
        Prints out all of the agent's stat information recorded throughout the mission.
        """
        agentId = self.agent.getId()
        fileName = agentId + "_" + datetime.fromtimestamp(time.time()).strftime('%m_%d_%Y_%H_%M_%S') + ".csv"
        filePath = "stats"
        if not os.path.isdir(filePath):
            os.mkdir(filePath)
        filePath = os.path.join(filePath, fileName)
        self.data.to_csv(filePath, index=False)
        print("{} stats output has been saved to: {}".format(agentId, filePath))


# ===========================================================================================================
# Standalone Functions
# ===========================================================================================================

def __getCSVFiles__():
    """
    Repeatedly asks the user to input the name of a stats CSV file in the stats directory, until the empty string is received.
    Returns the list of csv filenames.
    """
    filenames = []
    shouldGetInput = True
    while shouldGetInput:
        filename = input("Enter CSV file name: ")
        if len(filename) == 0:
            shouldGetInput = False
        else:
            filepath = os.path.join("stats", filename)
            if os.path.isfile(filepath):
                filenames.append(filename)
            else:
                print("'{}' could not be found.".format(filepath))
    return filenames

def __getGraphAttributes__():
    """
    Repeatedly collects attributes to plot from the user until an empty string is received.
    Returns the list of attributes.
    """
    print("Plottable Attributes ==============================")
    for i in attribute_names:
        print("- " + i)
    print("===================================================\n")
    
    attributes = []
    shouldGetInput = True
    while shouldGetInput:
        attribute = input("Attribute: ")
        if len(attribute) == 0:
            shouldGetInput = False
        else:
            attributes.append(attribute)
    return attributes

def main():
    """
    Main method allowing this file to be ran as a script for nicely outputting statistical data from a csv file in
    various forms.
    """
    filenames = __getCSVFiles__()
    if len(filenames) == 0:
        print("No CSV files entered")
        return

    # These have a 1:1 mapping to the filepaths gathered above
    agentDataList = []
    for filepath in filenames:
        agentData = AgentData(filepath.split("_")[0], pandas.read_csv(os.path.join("stats", filepath)))
        agentDataList.append(agentData)

    # Collect the attributes of interest in each AgentData object
    attributes = __getGraphAttributes__()

    # Plot each attribute against SysTime
    fig = plt.figure()
    fig.canvas.set_window_title("Agent Statistics Over Time")
    for agentData in agentDataList:
        for attribute in attributes:
            r = random.random()
            g = random.random()
            b = random.random()
            plt.plot(agentData.data["SysTime"], agentData.data[attribute], markeredgecolor=(r, g, b, 1), linestyle="solid", label="{} {}".format(agentData.agent_id, attribute))

    # Show the plot on-screen
    plt.legend(loc="best")
    plt.xlabel("Time")
    plt.ylabel("Amount")
    plt.show()


if __name__ == "__main__":
    main()