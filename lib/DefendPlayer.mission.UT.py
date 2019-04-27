#!/usr/bin/python
from __future__ import print_function
from builtins import range
import MalmoPython
import malmoutils
import os
import sys
import time
import json
import math
from collections import namedtuple
from Utils import *
from ScenarioBuilder import ScenarioBuilder
from Agent import *
from Logger import Logger
from Performance import Performance

MalmoPython.setLogging("", MalmoPython.LoggingSeverityLevel.LOG_OFF)

# SET UP ALL AGENT HOSTS & CLIENT POOL ==================================================================================
# Note: We only use one agent to parse command line options
player_agent = Agent("Player")
companion_agent = Agent("Companion")
malmoutils.parse_command_line(player_agent.host)
client_pool = MalmoPython.ClientPool()
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10000) )
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10001) )
# ========================================================================================================================

# SET UP THE ENVIRONMENT HERE ============================================================================================
scenarioBuilder = ScenarioBuilder("Defend Player", 30000, player_agent.getId(), Vector(0, 4, 0), Direction.North)
scenarioBuilder.addAgent(companion_agent.getId(), Vector(0, 4, 2), Direction.South)
scenarioBuilder.setTimeOfDay(TimeOfDay.Midnight)

# Player inventory
scenarioBuilder.agents[0].addInventoryItem(ItemType.All.diamond_helmet, ItemSlot.Armor.Helmet)
scenarioBuilder.agents[0].addInventoryItem(ItemType.All.diamond_chestplate, ItemSlot.Armor.Chestplate)
scenarioBuilder.agents[0].addInventoryItem(ItemType.All.diamond_leggings, ItemSlot.Armor.Leggings)
scenarioBuilder.agents[0].addInventoryItem(ItemType.All.diamond_boots, ItemSlot.Armor.Boots)

# Companion inventory
scenarioBuilder.agents[1].addInventoryItem(ItemType.All.diamond_helmet, ItemSlot.Armor.Helmet)
scenarioBuilder.agents[1].addInventoryItem(ItemType.All.diamond_chestplate, ItemSlot.Armor.Chestplate)
scenarioBuilder.agents[1].addInventoryItem(ItemType.All.diamond_leggings, ItemSlot.Armor.Leggings)
scenarioBuilder.agents[1].addInventoryItem(ItemType.All.diamond_boots, ItemSlot.Armor.Boots)
scenarioBuilder.agents[1].addInventoryItem(ItemType.All.diamond_sword, ItemSlot.HotBar._0)

# Structures
scenarioBuilder.environment.addCube(Vector(-100, 3, -100), Vector(100, 30, 100), BlockType.Stone)
scenarioBuilder.environment.addCube(Vector(-99, 4, -99), Vector(99, 29, 99), BlockType.Air)
for i in range(-99, 99):
    for j in range(-99, 99):
        if i % 4 == 0 and j % 4 == 0:
            scenarioBuilder.environment.addBlock(Vector(i, 4, j), BlockType.Torch)

# Zombie placements
scenarioBuilder.environment.addMob(Vector(2, 4, 4), MobType.Hostile.Zombie)
scenarioBuilder.environment.addMob(Vector(-20, 4, 20), MobType.Hostile.Zombie)
scenarioBuilder.environment.addMob(Vector(5, 4, -11), MobType.Hostile.Zombie)

missionXML = scenarioBuilder.finish()
# ========================================================================================================================

my_mission = MalmoPython.MissionSpec(missionXML, True)

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

# Not sure what the recording objects are for... but both use the agent host we said is parsing the command line options (see above)
safeStartMission(player_agent.host, my_mission, client_pool, malmoutils.get_default_recording_object(player_agent.host, "agent_1_viewpoint_continuous"), 0, '' )
safeStartMission(companion_agent.host, my_mission, client_pool, malmoutils.get_default_recording_object(player_agent.host, "agent_2_viewpoint_continuous"), 1, '' )
safeWaitForStart([player_agent.host, companion_agent.host])

# Specify which agents we want to track the performance of
Performance.addAgents([player_agent, companion_agent])

# Log initial state
Logger.trackClosestHostileMob(player_agent)
Logger.logInitialState(Agent.agentList)

# Wait for all agents to finish:
while player_agent.isMissionActive() or companion_agent.isMissionActive():
    # Update the performance of each agent
    Performance.update()

    # Ensure we have our diamond sword equipped
    companion_agent.equip(ItemType.All.diamond_sword)

    # If there is a zombie close to the player, target it for attack
    zombie = player_agent.getClosestHostileMob()
    if zombie != None:
        isLookingAt = companion_agent.lookAtEntity(zombie)
        if not isLookingAt:
            continue
        isAt = companion_agent.moveToEntity(zombie)
        if not isAt:
            continue
        companion_agent.attackMob(zombie)
        continue

    # No zombies nearby... return to player
    isLookingAt = companion_agent.lookAtAgent(player_agent)
    if not isLookingAt:
        continue
    isAt = companion_agent.moveToAgent(player_agent)
    if not isAt:
        continue

    # Nothing to do...
    companion_agent.stopAllMovement()

# Log final state and flush the log
Logger.logFinalState(Agent.agentList)
Logger.export()

# Export the performance of all agents
Performance.export()

print()
print("Mission ended")
