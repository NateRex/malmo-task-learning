# ==============================================================================================
# This file contains functionality for building up a scenario to be ran as a Malmo Python
# mission. Note: The only class in this file that should be used directly by callers is the
# ScenarioBuilder
# ==============================================================================================

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
    Internal class used by the ScenarioBuilder for developing XML for an agent in a Malmo mission
    """

    def __init__(self, name):
        self.name = name
        self.__position = (0, 0, 0)   # Each agent starts at the origin until specified otherwise
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
            <Placement x="{}" y="{}" z="{}" yaw="180"/>
            <Inventory>{}</Inventory>
        </AgentStart>
        <AgentHandlers>{}</AgentHandlers>
        </AgentSection>'''.format(self.name, str(self.__position[0]), str(self.__position[1]), str(self.__position[2]), self.__inventoryXML, self.__handlersXML)


class ScenarioBuilder:
    """
    Builder for creating a scenario in the form of a new Malmo mission. Decorations and agent attributes are
    set through the members of this object. Since it is possible to create scenarios with multiple agents, agents
    are stored in an array, which initially only has one agent. All points are specified as tuples in the form (x, y, z).
    """

    def __init__(self, description, timeLimit):
        # TODO: Change this to allow for multiple agents
        self.description = description
        self.timeLimit = timeLimit
        self.decorations = DecorationBuilder()
        self.agent = AgentBuilder("PlayerAgent")

    def finish(self):
        """Returns the complete XML string for the current scenario."""
        return '''
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
            
            {}
            </Mission>'''.format(self.description, self.decorations.finish(), str(self.timeLimit), self.agent.finish())