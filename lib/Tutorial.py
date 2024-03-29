from __future__ import print_function
from builtins import range
import MalmoPython
import malmoutils
import os
import sys
import time
import json
import math
from pynput.keyboard import Key, Controller
from collections import namedtuple
from Utils import *
from ScenarioBuilder import ScenarioBuilder
from Agent import *
from Logger import Logger
from Performance import Performance


MalmoPython.setLogging("", MalmoPython.LoggingSeverityLevel.LOG_OFF)

# SET UP ALL AGENT HOSTS & CLIENT POOL ==================================================================================
# Note: We only use one agent to parse command line options
player_agent = Agent("Player", AgentType.Human)
companion_agent = Agent("Companion", AgentType.Human)
malmoutils.parse_command_line(player_agent.host)
client_pool = MalmoPython.ClientPool()
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10000) )
client_pool.add( MalmoPython.ClientInfo('127.0.0.1',10001) )
# ========================================================================================================================

# SET UP THE ENVIRONMENT HERE ============================================================================================
scenarioBuilder = ScenarioBuilder("Learn How To Play", 1000000, player_agent.getId(), Vector(-15, 4, -16), Direction.North)
scenarioBuilder.addAgent(companion_agent.getId(), Vector(-15, 4, -10), Direction.North)
scenarioBuilder.environment.addBlock(Vector(-18, 4, -2), BlockType.Diamond_ore)
scenarioBuilder.environment.addMob(Vector(-10, 4, -35), MobType.Peaceful.Cow)

scenarioBuilder.setTimeOfDay(TimeOfDay.Noon)
scenarioBuilder.agents[1].addInventoryItem(ItemType.All.iron_pickaxe, ItemSlot.HotBar._4)
scenarioBuilder.agents[1].addInventoryItem(ItemType.All.stone_sword, ItemSlot.HotBar._5)

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

# Set up performance collection for all agents
Performance.filenameOverride = input("Enter a participant id: ")
print("CLICK INSIDE MINECRAFT WINDOW NOW")
for i in range(5):
    print(5 - i)
    time.sleep(1)

# Not sure what the recording objects are for... but both use the agent host we said is parsing the command line options (see above)
safeStartMission(player_agent.host, my_mission, client_pool, malmoutils.get_default_recording_object(player_agent.host, "agent_1_viewpoint_continuous"), 0, '' )
safeStartMission(companion_agent.host, my_mission, client_pool, malmoutils.get_default_recording_object(player_agent.host, "agent_2_viewpoint_continuous"), 1, '' )
safeWaitForStart([player_agent.host, companion_agent.host])

# Press enter within the window to activate the human controller
keyboard = Controller()
keyboard.press(Key.enter)
keyboard.release(Key.enter)

# Wait for all agents to finish:
while player_agent.isMissionActive() or companion_agent.isMissionActive():
    # Update the performance of each agent
    Performance.update()

# Export the performance of all agents
Performance.export()

print()
print("Mission ended")
