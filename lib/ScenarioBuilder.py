# ==============================================================================================
# This file contains functionality for building up a scenario to be ran as a Malmo Python
# mission. Note: The only class in this file that should be used directly by callers is the
# ScenarioBuilder
# ==============================================================================================
from Constants import *

class EnvironmentBuilder:
    """
    Internal class used by the ScenarioBuilder for developing XML for the environment of a Malmo mission
    """

    def __init__(self):
        self.__generatorString = "3;7,2*3,2;1;"
        self.__decoratorsXML = ""
        self.__allowedMobs = set([])

    def getAllowedMobsList(self):
        """
        Returns a list of strings representing all mobs that are allowed to spawn.
        """
        return self.__allowedMobs

    def turnOnAnimalSpawning(self):
        """
        Allow for the natural spawning of animals & villagers.
        """
        self.__allowedMobs.add(MobType.Pig.value)
        self.__allowedMobs.add(MobType.Sheep.value)
        self.__allowedMobs.add(MobType.Cow.value)
        self.__allowedMobs.add(MobType.Chicken.value)
        self.__allowedMobs.add(MobType.Ozelot.value)
        self.__allowedMobs.add(MobType.Rabbit.value)
        self.__allowedMobs.add(MobType.Villager.value)

    def turnOffAnimalSpawning(self):
        """
        Disallow the natural spawning of animals & villagers.
        """
        self.__allowedMobs.discard(MobType.Pig.value)
        self.__allowedMobs.discard(MobType.Sheep.value)
        self.__allowedMobs.discard(MobType.Cow.value)
        self.__allowedMobs.discard(MobType.Chicken.value)
        self.__allowedMobs.discard(MobType.Ozelot.value)
        self.__allowedMobs.discard(MobType.Rabbit.value)
        self.__allowedMobs.discard(MobType.Villager.value)

    def turnOnMonsterSpawning(self):
        """
        Allow for the natural spawning of monsters.
        """
        self.__allowedMobs.add(MobType.Spider.value)
        self.__allowedMobs.add(MobType.Zombie.value)
        self.__allowedMobs.add(MobType.Skeleton.value)
        self.__allowedMobs.add(MobType.Creeper.value)

    def turnOffMonsterSpawning(self):
        """
        Disallow for the natural spawning of monsters.
        """
        self.__allowedMobs.discard(MobType.Spider.value)
        self.__allowedMobs.discard(MobType.Zombie.value)
        self.__allowedMobs.discard(MobType.Skeleton.value)
        self.__allowedMobs.discard(MobType.Creeper.value)

    def addCube(self, point0, point1, blockType, variant = None):
        """
        Add a cuboid of a specific block type from lower-left-near corner point0 to upper-right-far corner point1.
        Each point is specified as an (x, y, z) tuple. If the block type specified is a mob spawner an additional mob type
        must be provided.
        """
        if (blockType == BlockType.Mob_spawner):
            if (variant != None):
                self.__allowedMobs.add(variant.value)   # Ensure the mob is allowed to spawn
                self.__decoratorsXML += '''<DrawCuboid x1="{}" y1="{}" z1="{}" x2="{}" y2="{}" z2="{}" type="{}" variant="{}"/>'''.format(point0[0], point0[1], point0[2], point1[0], point1[1], point1[2], blockType.value, variant.value)
        else:
            self.__decoratorsXML += '''<DrawCuboid x1="{}" y1="{}" z1="{}" x2="{}" y2="{}" z2="{}" type="{}"/>'''.format(point0[0], point0[1], point0[2], point1[0], point1[1], point1[2], blockType.value)

    def addLine(self, point0, point1, blockType, variant = None):
        """
        Add a line of a specific block type from point0 to point1, where each point is specified as an (x, y, z) tuple.
        If the block type specified is a mob spawner, an additional mob type must be provided.
        """
        if (blockType == BlockType.Mob_spawner):
            if (variant != None):
                self.__allowedMobs.add(variant.value)   # Ensure the mob is allowed to spawn
                self.__decoratorsXML += '''<DrawLine x1="{}" y1="{}" z1="{}" x2="{}" y2="{}" z2="{}" type="{}" variant="{}"/>'''.format(point0[0], point0[1], point0[2], point1[0], point1[1], point1[2], blockType.value, variant.value)
        else:
            self.__decoratorsXML += '''<DrawLine x1="{}" y1="{}" z1="{}" x2="{}" y2="{}" z2="{}" type="{}"/>'''.format(point0[0], point0[1], point0[2], point1[0], point1[1], point1[2], blockType.value)

    def addBlock(self, location, blockType, variant = None):
        """
        Add a block of a specific type at the location specified. The location should be given as an (x, y, z) tuple.
        If the block type specified is a mob spawner, an additional mob type must be provided.
        """
        if (blockType == BlockType.Mob_spawner):
            if (variant != None):
                self.__allowedMobs.add(variant.value)   # Ensure the mob is allowed to spawn
                self.__decoratorsXML += '''<DrawBlock x="{}" y="{}" z="{}" type="{}" variant="{}"/>'''.format(location[0], location[1], location[2], blockType.value, variant.value)
        else:
            self.__decoratorsXML += '''<DrawBlock x="{}" y="{}" z="{}" type="{}"/>'''.format(location[0], location[1], location[2], blockType.value)

    def addSphere(self, center, radius, blockType, variant = None):
        """
        Add a sphere of a specific block type, with a given radius and center. The center should be given as an (x, y, z) tuple.
        If the block type specified is a mob spawner, an additional mob type must be provided.
        """
        if (blockType == BlockType.Mob_spawner):
            if (variant != None):
                self.__allowedMobs.add(variant.value)   # Ensure the mob is allowed to spawn
                self.__decoratorsXML += '''<DrawSphere x="{}" y="{}" z="{}" radius="{}" type="{}" variant="{}"/>'''.format(center[0], center[1], center[2], radius, blockType.value, variant.value)
        else:
            self.__decoratorsXML += '''<DrawSphere x="{}" y="{}" z="{}" radius="{}" type="{}"/>'''.format(center[0], center[1], center[2], radius, blockType.value)

    def addDropItem(self, location, itemType):
        """
        Add a drop-item at a specific location specified as an (x, y, z) tuple.
        """
        self.__decoratorsXML += '''<DrawItem x="{}" y="{}" z="{}" type="{}"/>'''.format(location[0], location[1], location[2], itemType.value)

    def finish(self):
        """
        Return the complete XML string for this set of decorations
        """
        return '''
        <FlatWorldGenerator generatorString="{}"/>
        {}
        '''.format(self.__generatorString, "<DrawingDecorator>" + self.__decoratorsXML + "</DrawingDecorator>" if len(self.__decoratorsXML) > 0 else "")
    

class AgentBuilder:
    """
    Internal class used by the ScenarioBuilder for developing XML for an agent in a Malmo mission.
    """

    def __init__(self, name, startPosition = None, startDirection = None):
        self.name = name
        self.__position = startPosition if startPosition != None else (0, 0, 0)
        self.__direction = startDirection.value if startDirection != None else Direction.North.value
        self.__inventoryXML = ""
        self.__handlersXML = ""

    def setPosition(self, position):
        """
        Set the position of this agent in world-space given an (x, y, z) tuple.
        """
        self.__position = position

    def getPosition(self):
        """
        Returns the position of this agent in world-space as an (x, y, z) tuple.
        """
        return self.__position

    def setDirection(self, direction):
        """
        Set the direction for this agent to face (North, South, East, West).
        """
        self.__direction = direction.value

    def getDirection(self):
        """
        Returns the starting direction this agent is currently set to face as an integer value representing the yaw angle in degrees.
        """
        return self.__direction
    
    def addInventoryItem(self, item, slot):
        """
        Add an item to this agent's inventory at the designated item slot number.
        Each agent has 39 item slots, where 0-8 are the hotbar slots, 9-35 are the inventory slots, and 36-39 are the armor slots.
        """
        self.__inventoryXML += '''<InventoryItem slot="{}" type="{}"/>'''.format(slot.value, item.value)


    def finish(self):
        """
        Returns the complete XML string for this agent being built.
        """
        return '''
        <AgentSection mode="Survival">
        <Name>{}</Name>
        <AgentStart>
            <Placement x="{}" y="{}" z="{}" yaw="{}"/>
            <Inventory>
            {}
            </Inventory>
        </AgentStart>
        <AgentHandlers>
        {}
        </AgentHandlers>
        </AgentSection>'''.format(self.name, str(self.__position[0]), str(self.__position[1]), str(self.__position[2]), str(self.__direction), self.__inventoryXML, self.__handlersXML)


class ScenarioBuilder:
    """
    Builder for creating a new Malmo mission scenario. Environment and agent attributes are
    set through members of this object. Every scenario starts with one agent. Upon creating a new ScenarioBuilder, optionally
    specify a name, starting position, and direction for this agent, otherwise, they will default to "Agent", the origin (0, 0, 0), and
    north, respectively.
    """

    def __init__(self, description, timeLimit, agentName = "Agent", startPosition = None, startDirection = None):
        self.__description = description
        self.__timeLimit = timeLimit
        self.__timeOfDay = TimeOfDay.Noon.value
        self.environment = EnvironmentBuilder()
        self.agents = [AgentBuilder(agentName, startPosition, startDirection)]

    def setDescription(self, description):
        """
        Set a description for this specific scenario.
        """
        self.__description = description

    def setTimeLimit(self, timeLimit):
        """
        Set a time limit for the mission to run.
        """
        self.__timeLimit = timeLimit

    def setTimeOfDay(self, timeOfDay):
        """
        Set the time of day for this scenario.
        """
        self.__timeOfDay = timeOfDay.value

    def addAgent(self, name, startPosition = None, startDirection = Direction.North):
        """
        Add a new agent to this scenario, giving it a name.
        Optionally specify a starting location as an (x, y, z) tuple, as well as a direction.
        Otherwise, the agent will start at the origin (0, 0, 0) facing north.
        """
        self.agents.append(AgentBuilder(name, startPosition, startDirection))

    def finish(self):
        """
        Returns the complete XML string for the current scenario.
        """
        mobsList = self.environment.getAllowedMobsList()
        mobsAllowed = ""
        for mob in mobsList:
            mobsAllowed = mobsAllowed + mob + " "
        returnValue = '''
        <?xml version="1.0" encoding="UTF-8" standalone="no" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <About>
                <Summary>{}</Summary>
            </About>

            <ServerSection>
                    <ServerInitialConditions>
                        <Time>
                            <StartTime>{}</StartTime>
                            <AllowPassageOfTime>false</AllowPassageOfTime>
                        </Time>
                        <Weather>clear</Weather>
                        <AllowSpawning>{}</AllowSpawning>
                        <AllowedMobs>{}</AllowedMobs>
                    </ServerInitialConditions>
            
                <ServerHandlers>
                        {}
                        <ServerQuitFromTimeUp timeLimitMs="{}"/>
                    <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
            </ServerSection>
            '''.format(self.__description, self.__timeOfDay, "false" if len(mobsList) == 0 else "true", mobsAllowed, self.environment.finish(), str(self.__timeLimit))
        for i in range(0, len(self.agents)):
            returnValue += self.agents[i].finish()
        return returnValue + "</Mission>"