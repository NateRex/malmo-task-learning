# ==============================================================================================
# In this mission, the companion and agent spawn in a large dark corridor. The companion must
# fend off zombies that are approaching and defend the player.
# ==============================================================================================
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
from Constants import *
from Utils import *
from ScenarioBuilder import *
from Agent import *
from Logger import *

MalmoPython.setLogging("", MalmoPython.LoggingSeverityLevel.LOG_OFF)

# SET UP ALL AGENT HOSTS & CLIENT POOL ==================================================================================
# Note: We only use one agent to parse command line options
player_agent = Agent()
companion_agent = Agent()
malmoutils.parse_command_line(player_agent.host)
client_pool = MalmoPython.ClientPool()
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10000) )
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10001) )
# ========================================================================================================================

# SET UP THE ENVIRONMENT HERE ============================================================================================
# Player Agent
scenarioBuilder = ScenarioBuilder("Test Scenario", 25000, "Player", Vector(0, 4, 0), Direction.North)
scenarioBuilder.addAgent("Companion", Vector(0, 4, -15), Direction.South)

scenarioBuilder.setTimeOfDay(TimeOfDay.Noon)
scenarioBuilder.environment.addLine(Vector(-3, 4, 1), Vector(-3, 4, -25), BlockType.Fence)
scenarioBuilder.environment.addLine(Vector(3, 4, 1), Vector(3, 4, -25), BlockType.Fence)
scenarioBuilder.environment.addLine(Vector(-2, 4, 1), Vector(2, 4, 1), BlockType.Fence)
scenarioBuilder.environment.addLine(Vector(-2, 4, -25), Vector(2, 4, -25), BlockType.Fence)
scenarioBuilder.environment.addBlock(Vector(0, 3, -22), BlockType.Mob_spawner, MobType.Peaceful.Pig)

scenarioBuilder.agents[1].addInventoryItem(ItemType.All.diamond, ItemSlot.HotBar._3, 6)
scenarioBuilder.agents[1].addInventoryItem(ItemType.All.stick, ItemSlot.HotBar._4, 3)
scenarioBuilder.agents[1].addInventoryItem(ItemType.All.diamond_boots, ItemSlot.Armor.Boots)
scenarioBuilder.agents[1].addInventoryItem(ItemType.All.diamond_leggings, ItemSlot.Armor.Leggings)
scenarioBuilder.agents[1].addInventoryItem(ItemType.All.diamond_chestplate, ItemSlot.Armor.Chestplate)
scenarioBuilder.agents[1].addInventoryItem(ItemType.All.diamond_helmet, ItemSlot.Armor.Helmet)

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
Logger.logInitialState([companion_agent, player_agent])

numberOfSwordsCrafted = 0

# Wait for all agents to finish:
while player_agent.isMissionActive() or companion_agent.isMissionActive():
    # AGENT ACTIONS GO HERE  =============================================================================================
    if numberOfSwordsCrafted < 3:
        companion_agent.craft(ItemType.All.diamond_sword, [RecipeItem(ItemType.All.diamond, 2), RecipeItem(ItemType.All.stick, 1)])
        numberOfSwordsCrafted += 1
        continue

    nearestPig = companion_agent.getClosestFoodMob()
    if nearestPig == None:
        companion_agent.stopAllMovement()
        continue

    # Look at nearest pig
    isLookingAt = companion_agent.lookAtEntity(nearestPig)
    if not isLookingAt:
        companion_agent.stopMoving()
        companion_agent.stopAttacking()
        continue
    
    # Move to nearest pig
    isAt = companion_agent.moveToEntity(nearestPig)
    if not isAt:
        companion_agent.stopAttacking()
        continue
    
    # Attack the nearest pig
    companion_agent.attackMob(nearestPig)
    # ====================================================================================================================

# Log final state and flush the log
Logger.logFinalState()
Logger.flushToFile()
print()
print("Mission ended")
