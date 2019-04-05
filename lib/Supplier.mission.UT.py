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
# Player Agent
scenarioBuilder = ScenarioBuilder("Supply Materials", 30000, player_agent.getId(), Vector(0, 4, 0), Direction.North)
scenarioBuilder.addAgent(companion_agent.getId(), Vector(0, 4, 4), Direction.North)
scenarioBuilder.setTimeOfDay(TimeOfDay.Noon)

scenarioBuilder.agents[0].addInventoryItem(BlockType.Cobblestone, ItemSlot.HotBar._0, 20)
scenarioBuilder.agents[0].addInventoryItem(BlockType.Quartz_block, ItemSlot.HotBar._1, 15)
scenarioBuilder.agents[0].addInventoryItem(ItemType.All.diamond_pickaxe, ItemSlot.HotBar._8)
scenarioBuilder.agents[1].addInventoryItem(ItemType.All.iron_pickaxe, ItemSlot.HotBar._0)

# Randomly generate small towers of blocks behind the companion
towersGenerated = 0
miscBlocks = [BlockType.Emerald_block, BlockType.Lapis_ore, BlockType.Mossy_cobblestone, BlockType.Stained_glass, BlockType.Brick_block]
while (towersGenerated < 13):
    for x in range(-15, 26):
        for z in range(15, 40):
            rand = random.randint(1, 21)
            if (rand != 1):
                continue

            for y in range(4, 7):
                rand = random.randint(1, 4)
                if rand == 1:
                    scenarioBuilder.environment.addBlock(Vector(x, y, z), BlockType.Cobblestone)
                elif rand == 2:
                    scenarioBuilder.environment.addBlock(Vector(x, y, z), BlockType.Quartz_block)
                else:
                    scenarioBuilder.environment.addBlock(Vector(x, y, z), random.choice(miscBlocks))
            towersGenerated += 1

# Add a special block where whichever block type sits on top of it is the one the companion will fetch
scenarioBuilder.environment.addBlock(Vector(-4, 4, -2), BlockType.Diamond_block)

# Set the starting "collection block" to be gold (something not currently in the environment)
scenarioBuilder.environment.addBlock(Vector(-4, 5, -2), BlockType.Beacon)

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

# Log initial state
Logger.logInitialState(Agent.agentList)

while player_agent.isMissionActive() or companion_agent.isMissionActive():
    # Check if there is anything on the signaling block
    diamondBlock = player_agent.getClosestBlockByType(BlockType.Diamond_block)
    print("{} is at {}".format(diamondBlock.type, diamondBlock.position))
    specialLoc = Vector(diamondBlock.position.x, diamondBlock.position.y + 1, diamondBlock.position.z)
    blockType = player_agent.getBlockTypeAtLocation(specialLoc)
    print("{} is at {}".format(blockType.value, specialLoc))

    # Nothing to do...
    companion_agent.noAction()

# Log final state and flush the log
Logger.logFinalState(Agent.agentList)
Logger.export()
print()
print("Mission ended")
