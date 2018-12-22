from __future__ import print_function
from builtins import range
import MalmoPython
import malmoutils
import os
import sys
import time
from Utils import *
from Agent import *
from ScenarioBuilder import *

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
#scenarioBuilder = ScenarioBuilder("Test Scenario", 40000, "Player", Vector(0, 5, 0), Direction.North)
scenarioBuilder = ScenarioBuilder("Test Scenario", 40000, "Player", Vector(0, 5, 0), Direction.North)
scenarioBuilder.addAgent("Companion", Vector(0.5, 5, -3.5), Direction.North)

scenarioBuilder.setTimeOfDay(TimeOfDay.Noon)
scenarioBuilder.environment.addCube(Vector(-3, 4, 2), Vector(3, 8, -35), BlockType.Mossy_cobblestone)
scenarioBuilder.environment.addCube(Vector(-2, 5, 1), Vector(2, 7, -34), BlockType.Air)
scenarioBuilder.environment.addBlock(Vector(0, 4, -5), BlockType.Diamond_block)
#scenarioBuilder.environment.addBlock(Vector(2, 4, -7), BlockType.Diamond_block)
#scenarioBuilder.environment.addBlock(Vector(-2, 4, -7), BlockType.Diamond_block)
scenarioBuilder.environment.addMob(Vector(-1, 5, -33), MobType.Hostile.Zombie)
scenarioBuilder.environment.addMob(Vector(1, 5, -33), MobType.Hostile.Zombie)
scenarioBuilder.environment.addMob(Vector(0, 5, -25), MobType.Hostile.Zombie)
scenarioBuilder.environment.turnOffAnimalSpawning()
scenarioBuilder.environment.turnOffMonsterSpawning()
for i in range(0, 31):
    if i % 5 == 0:
        scenarioBuilder.environment.addBlock(Vector(-3, 6, -i), BlockType.Torch)
        scenarioBuilder.environment.addBlock(Vector(3, 6, -i), BlockType.Torch)

scenarioBuilder.agents[1].addInventoryItem(ItemType.All.diamond_sword, ItemSlot.HotBar._0)
#scenarioBuilder.agents[1].addInventoryItem(ItemType.Diamond_boots, ItemSlot.Armor.Boots)
#scenarioBuilder.agents[1].addInventoryItem(ItemType.Diamond_leggings, ItemSlot.Armor.Leggings)
#scenarioBuilder.agents[1].addInventoryItem(ItemType.Diamond_chestplate, ItemSlot.Armor.Chestplate)
#scenarioBuilder.agents[1].addInventoryItem(ItemType.Diamond_helmet, ItemSlot.Armor.Helmet)

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
    time_out = 50  # Allow two minutes for mission to start.
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

# Log Initial State
Logger.logInitialState([companion_agent, player_agent])

# Used to calculate time of previous attack
start_time = time.time()

# Wait for all agents to finish:
while player_agent.isMissionActive() or companion_agent.isMissionActive():
    # AGENT ACTIONS GO HERE  =============================================================================================

    player_agent.stats.checkHealth(player_agent)
    companion_agent.stats.checkHealth(companion_agent)

    # Agent Code
    nearestZombie = companion_agent.getClosestHostileMob()
    if nearestZombie != None:
        companion_agent.stopAllMovement()
        companion_agent.lookAtEntity(nearestZombie)
        companion_agent.attackMob(nearestZombie)
    else:
        nearestBlock = companion_agent.getClosestBlockLocation(BlockType.Diamond_block)
        if nearestBlock != None:
            lookingAt = companion_agent.lookAtEntity(nearestBlock)
            if lookingAt:
                companion_agent.stopTurning()
                companion_agent.moveToMob(nearestBlock)
            else:
                companion_agent.stopAllMovement()
                companion_agent.stopTurning()

    # ====================================================================================================================

print()
player_agent.stats.logStats(player_agent)
companion_agent.stats.logStats(companion_agent)
companion_agent.stats.printStats(companion_agent)
player_agent.stats.printStats(player_agent)

# Log final state and flush the log
Logger.logFinalState()
# Logger.flushToFile()
print("Mission ended")
