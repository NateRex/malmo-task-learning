# ==============================================================================================
# This file serves as an example of how to set up a scenario for the Malmo platform. The XML for
# the environment and agent settings is dynamically generated using the ScenarioBuilder in
# ScenarioBuilder.py.
# ==============================================================================================
from __future__ import print_function
from builtins import range
import MalmoPython
import malmoutils
import os
import sys
import time
from Constants import *
from ScenarioBuilder import ScenarioBuilder

# SET UP ALL AGENT HOSTS =================================================================================================
companion_host = MalmoPython.AgentHost()
player_host = MalmoPython.AgentHost()
# ========================================================================================================================

# Use companion_host for parsing the command-line options.
malmoutils.parse_command_line(companion_host)

# SET UP THE ENVIRONMENT HERE ============================================================================================
# Companion Agent
companionPos = (0, 5, 0)
scenarioBuilder = ScenarioBuilder("Test Scenario", 10000, "Companion", (0.5, 5, 0.5), Direction.North) # We adjust agent start position by 0.5 in x & z to start the agent in the CENTER of the block
scenarioBuilder.agents[0].addInventoryItem(ItemType.Diamond_sword, ItemSlot.HotBar._0)
scenarioBuilder.agents[0].addInventoryItem(ItemType.Diamond_boots, ItemSlot.Armor.Boots)
scenarioBuilder.agents[0].addInventoryItem(ItemType.Diamond_leggings, ItemSlot.Armor.Leggings)
scenarioBuilder.agents[0].addInventoryItem(ItemType.Diamond_chestplate, ItemSlot.Armor.Chestplate)
scenarioBuilder.agents[0].addInventoryItem(ItemType.Diamond_helmet, ItemSlot.Armor.Helmet)

# Player Agent
playerPos = (0, 3, -9)
scenarioBuilder.addAgent("Player", (0.5, 3, -8.5), Direction.South)
scenarioBuilder.agents[1].addInventoryItem(ItemType.Stone_pickaxe, ItemSlot.HotBar._0)
scenarioBuilder.agents[1].addInventoryItem(ItemType.Leather_boots, ItemSlot.Armor.Boots)
scenarioBuilder.agents[1].addInventoryItem(ItemType.Leather_leggings, ItemSlot.Armor.Leggings)
scenarioBuilder.agents[1].addInventoryItem(ItemType.Leather_chestplate, ItemSlot.Armor.Chestplate)
scenarioBuilder.agents[1].addInventoryItem(ItemType.Leather_helmet, ItemSlot.Armor.Helmet)

# Mobs
scenarioBuilder.setTimeOfDay(TimeOfDay.Dawn)
scenarioBuilder.environment.addBlock((13, 3, 0), BlockType.Mob_spawner, MobType.Pig)
scenarioBuilder.environment.addBlock((-13, 3, 0), BlockType.Mob_spawner, MobType.Pig)
scenarioBuilder.environment.addBlock((0, 3, 13), BlockType.Mob_spawner, MobType.Pig)

# Decorations
scenarioBuilder.environment.addSphere((0, 40, 0), 39, BlockType.Air)
scenarioBuilder.environment.addLine((0, 0, 0), (0, 4, 0), BlockType.Gold_block)
scenarioBuilder.environment.addCube((companionPos[0] - 20, 1, companionPos[2] - 20), (companionPos[0] + 20, 1, companionPos[2] + 20), BlockType.Lava)
scenarioBuilder.environment.addCube((companionPos[0] - 2, 1, companionPos[2] - 2), (companionPos[0] + 2, 1, companionPos[2] + 2), BlockType.Stone)
for i in range(-5, 6):
    for j in range(-5, 6):
        scenarioBuilder.environment.addDropItem((companionPos[0] + i, 35, companionPos[2] + j), ItemType.Emerald)
missionXML = scenarioBuilder.finish()
print(missionXML)
# ========================================================================================================================

my_mission = MalmoPython.MissionSpec(missionXML, True)

# Add clients to client pool =============================================================================================
# Note: We have one for each agent, since each agent needs its own client running
client_pool = MalmoPython.ClientPool()
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10000) )
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10001) )
# ========================================================================================================================

MalmoPython.setLogging("", MalmoPython.LoggingSeverityLevel.LOG_OFF)

def safeStartMission(agent_host, mission, client_pool, recording, role, experimentId):
    used_attempts = 0
    max_attempts = 5
    print("Calling startMission for role", role)
    while True:
        try:
            agent_host.startMission(mission, client_pool, recording, role, experimentId)
            break
        except MalmoPython.MissionException as e:
            errorCode = e.details.errorCode
            if errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_WARMING_UP:
                print("Server not quite ready yet - waiting...")
                time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_INSUFFICIENT_CLIENTS_AVAILABLE:
                print("Not enough available Minecraft instances running.")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait in case they are starting up.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            elif errorCode == MalmoPython.MissionErrorCode.MISSION_SERVER_NOT_FOUND:
                print("Server not found - has the mission with role 0 been started yet?")
                used_attempts += 1
                if used_attempts < max_attempts:
                    print("Will wait and retry.", max_attempts - used_attempts, "attempts left.")
                    time.sleep(2)
            else:
                print("Other error:", e.message)
                print("Waiting will not help here - bailing immediately.")
                exit(1)
        if used_attempts == max_attempts:
            print("All chances used up - bailing now.")
            exit(1)
    print("startMission called okay.")

def safeWaitForStart(agent_hosts):
    print("Waiting for the mission to start", end=' ')
    start_flags = [False for a in agent_hosts]
    start_time = time.time()
    time_out = 120  # Allow two minutes for mission to start.
    while not all(start_flags) and time.time() - start_time < time_out:
        states = [a.peekWorldState() for a in agent_hosts]
        start_flags = [w.has_mission_begun for w in states]
        errors = [e for w in states for e in w.errors]
        if len(errors) > 0:
            print("Errors waiting for mission start:")
            for e in errors:
                print(e.text)
            print("Bailing now.")
            exit(1)
        time.sleep(0.1)
        print(".", end=' ')
    print()
    if time.time() - start_time >= time_out:
        print("Timed out waiting for mission to begin. Bailing.")
        exit(1)
    print("Mission has started.")

# Not sure what the recording objects are for... but both use the host we said is parsing the command line options (see above)
safeStartMission(companion_host, my_mission, client_pool, malmoutils.get_default_recording_object(companion_host, "agent_1_viewpoint_discrete"), 0, '' )
safeStartMission(player_host, my_mission, client_pool, malmoutils.get_default_recording_object(companion_host, "agent_2_viewpoint_discrete"), 1, '' )
safeWaitForStart([companion_host, player_host])

# AGENT ACTIONS GO HERE ==================================================================================================

# ========================================================================================================================

# Wait for all agents to finish:
while player_host.peekWorldState().is_mission_running or companion_host.peekWorldState().is_mission_running:
    time.sleep(1)

print()
print("Mission ended")
# Mission has ended.
