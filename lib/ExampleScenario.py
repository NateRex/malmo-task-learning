# ==============================================================================================
# This file serves as an example of how to set up a scenario for the Malmo platform. The XML for
# the environment and agent settings is dynamically generated using the ScenarioBuilder in
# ScenarioBuilder.py.
# ==============================================================================================
from __future__ import print_function
from builtins import range
import MalmoPython
import os
import sys
import time

from Constants import BlockType, ItemType, ItemSlot
from ScenarioBuilder import ScenarioBuilder

if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# SET UP THE ENVIRONMENT HERE ============================================================================================
# Agent
scenarioBuilder = ScenarioBuilder("Test Scenario", 10000)
agentPosition = (0, 5, 0)
scenarioBuilder.agent.setPosition((0.5, 5, 0.5))    # We adjust by 0.5 to start the agent in the CENTER of the block
scenarioBuilder.agent.addInventoryItem(ItemType.Diamond_sword, ItemSlot.HotBar._0)
scenarioBuilder.agent.addInventoryItem(ItemType.Diamond_boots, ItemSlot.Armor.Boots)
scenarioBuilder.agent.addInventoryItem(ItemType.Diamond_leggings, ItemSlot.Armor.Leggings)
scenarioBuilder.agent.addInventoryItem(ItemType.Diamond_chestplate, ItemSlot.Armor.Chestplate)
scenarioBuilder.agent.addInventoryItem(ItemType.Diamond_helmet, ItemSlot.Armor.Helmet)

# Decorations
scenarioBuilder.decorations.addSphere((0, 40, 0), 39, BlockType.Air)
scenarioBuilder.decorations.addLine((0, 0, 0), (0, 4, 0), BlockType.Gold_block)
scenarioBuilder.decorations.addCube((agentPosition[0] - 20, 1, agentPosition[2] - 20), (agentPosition[0] + 20, 1, agentPosition[2] + 20), BlockType.Lava)
scenarioBuilder.decorations.addCube((agentPosition[0] - 2, 1, agentPosition[2] - 2), (agentPosition[0] + 2, 1, agentPosition[2] + 2), BlockType.Stone)
for i in range(-5, 6):
    for j in range(-5, 6):
        scenarioBuilder.decorations.addDropItem((agentPosition[0] + i, 35, agentPosition[2] + j), ItemType.Emerald)
missionXML = scenarioBuilder.finish()
# ========================================================================================================================

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission running ", end=' ')

# AGENT ACTIONS GO HERE ==================================================================================================

# ========================================================================================================================

# Loop until mission ends:
while world_state.is_mission_running:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:",error.text)

print()
print("Mission ended")
# Mission has ended.
