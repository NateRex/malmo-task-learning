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
player_agent = Agent("Player", AgentType.Hardcoded)
companion_agent = Agent("Companion", AgentType.Hardcoded)
malmoutils.parse_command_line(player_agent.host)
client_pool = MalmoPython.ClientPool()
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10000) )
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10001) )
# ========================================================================================================================

# SET UP THE ENVIRONMENT HERE ============================================================================================
# Player Agent
scenarioBuilder = ScenarioBuilder("Hunt For Food", 30000, player_agent.getId(), Vector(-15, 4, -16), Direction.North)
scenarioBuilder.addAgent(companion_agent.getId(), Vector(-15, 4, -15), Direction.South)

scenarioBuilder.setTimeOfDay(TimeOfDay.Noon)

scenarioBuilder.environment.addLine(Vector(-20, 4, -1), Vector(-20, 4, -20), BlockType.Fence)
scenarioBuilder.environment.addLine(Vector(3, 4, -1), Vector(3, 4, -20), BlockType.Fence)
scenarioBuilder.environment.addLine(Vector(-19, 4, -2), Vector(2, 4, -2), BlockType.Fence)
scenarioBuilder.environment.addLine(Vector(-19, 4, -20), Vector(2, 4, -20), BlockType.Fence)

scenarioBuilder.environment.addMob(Vector(-10, 4, -10), MobType.Peaceful.Cow)
scenarioBuilder.environment.addMob(Vector(-10, 4, -15), MobType.Peaceful.Cow)

scenarioBuilder.agents[1].addInventoryItem(ItemType.All.diamond_sword, ItemSlot.HotBar._0)

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

# Set up the Performance collector
Performance.trackItems([ItemType.Food.beef])
Performance.addAgents([player_agent, companion_agent])

# Log initial state
Logger.trackClosestFoodMob(companion_agent)
Logger.trackClosestFoodItem(companion_agent)
Logger.trackInventory(companion_agent)
Logger.logInitialState(Agent.agentList)

# Wait for all agents to finish:
while player_agent.isMissionActive() or companion_agent.isMissionActive():
    Performance.update()

    # If we have beef, go to the player and give it to them
    if companion_agent.inventory.amountOfItem(ItemType.Food.beef) > 0:
        isLookingAt = companion_agent.lookAtAgent(player_agent)
        if not isLookingAt:
            continue
        isAt = companion_agent.moveToAgent(player_agent)
        if not isAt:
            continue
        companion_agent.equip(ItemType.Food.beef)
        companion_agent.giveItemToAgent(ItemType.Food.beef, player_agent)
        continue

    # If there is beef laying on the ground nearby, go pick it up
    closestFood = companion_agent.getClosestFoodItem()
    if closestFood != None:
        didPickUp = companion_agent.pickUpItem(closestFood)
        if not didPickUp:
            continue
        continue

    # If there are cows nearby, go and harvest them
    companion_agent.equip(ItemType.All.diamond_sword)   # Make sure we have our diamond sword equipped
    closestCow = companion_agent.getClosestFoodMob()
    if closestCow != None:
        isLookingAt = companion_agent.lookAtEntity(closestCow)
        if not isLookingAt:
            continue
        isAt = companion_agent.moveToEntity(closestCow)
        if not isAt:
            continue
        didAttack = companion_agent.attackMob(closestCow)
        if not didAttack:
            continue
        continue
    
    # Nothing to do...
    companion_agent.noAction()

# Log final state and flush the log
Logger.logFinalState(Agent.agentList)
Logger.export()

# Export the performance data for all agents
Performance.export()

print()
print("Mission ended")
