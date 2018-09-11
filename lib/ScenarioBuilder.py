# ==============================================================================================
# This file contains functionality for building up a scenario to be ran as a Malmo Python
# mission. Note: The only class in this file that should be used directly by callers is the
# ScenarioBuilder
# ==============================================================================================
from Constants import Direction

class DecorationBuilder:
    """
    Internal class used by the ScenarioBuilder for developing XML for the environment of a Malmo mission
    """

    def __init__(self):
        self.__generatorString = "3;7,2*3,2;1;"
        self.__decoratorsXML = ""

    def addCube(self, point0, point1, blockType):
        """
        Add a cuboid of a specific block type from lower-left-near corner point0 to upper-right-far corner point1.
        Each point is specified as an (x, y, z) tuple.
        """
        self.__decoratorsXML += '''<DrawCuboid x1="{}" y1="{}" z1="{}" x2="{}" y2="{}" z2="{}" type="{}"/>'''.format(point0[0], point0[1], point0[2], point1[0], point1[1], point1[2], blockType.value)

    def addLine(self, point0, point1, blockType):
        """
        Add a line of a specific block type from point0 to point1, where each point is specified as an (x, y, z) tuple.
        """
        self.__decoratorsXML += '''<DrawLine x1="{}" y1="{}" z1="{}" x2="{}" y2="{}" z2="{}" type="{}"/>'''.format(point0[0], point0[1], point0[2], point1[0], point1[1], point1[2], blockType.value)

    def addBlock(self, location, blockType):
        """
        Add a block of a specific type at the location specified. The location should be given as an (x, y, z) tuple.
        """
        self.__decoratorsXML += '''<DrawBlock x="{}" y="{}" z="{}" type="{}"/>'''.format(location[0], location[1], location[2], blockType.value)

    def addSphere(self, center, radius, blockType):
        """
        Add a sphere of a specific block type, with a given radius and center. The center should be given as an (x, y, z) tuple.
        """
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
    Builder for creating a new Malmo mission scenario. Decorations and agent attributes are
    set through members of this object. Every scenario starts with one agent. Upon creating a new ScenarioBuilder, optionally
    specify a name, starting position, and direction for this agent, otherwise, they will default to "Agent", the origin (0, 0, 0), and
    north, respectively.
    """

    def __init__(self, description, timeLimit, agentName = "Agent", startPosition = None, startDirection = None):
        self.description = description
        self.timeLimit = timeLimit
        self.decorations = DecorationBuilder()
        self.agents = [AgentBuilder(agentName, startPosition, startDirection)]

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
        returnValue = '''
        <?xml version="1.0" encoding="UTF-8" standalone="no" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <About>
                <Summary>{}</Summary>
            </About>

            <ServerSection>
                    <ServerInitialConditions>
                        <Time>
                            <StartTime>1000</StartTime>
                            <AllowPassageOfTime>false</AllowPassageOfTime>
                        </Time>
                        <Weather>clear</Weather>
                    </ServerInitialConditions>
            
                <ServerHandlers>
                        {}
                        <ServerQuitFromTimeUp timeLimitMs="{}"/>
                    <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
            </ServerSection>
            '''.format(self.description, self.decorations.finish(), str(self.timeLimit))
        for i in range(0, len(self.agents)):
            returnValue += self.agents[i].finish()
        return returnValue + "</Mission>"