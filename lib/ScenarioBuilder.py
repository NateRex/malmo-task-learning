# ==============================================================================================
# This file contains functionality for building up a scenario to be ran as a Malmo Python
# mission. Note: The only class in this file that should be used directly by callers is the
# ScenarioBuilder
# ==============================================================================================

def translatePoint(origin, point):
    """
    Translate a point in space by the given origin of a coordinate system.
    """
    return (point[0] + origin[0], point[1] + origin[1], point[2] + origin[2])

class DecorationBuilder:
    """
    Internal class used by the ScenarioBuilder for developing XML for the environment of a Malmo mission
    """

    def __init__(self, origin):
        self.__origin = origin   # (x, y, z)
        self.__generatorString = "3;7,2*3,2;1;"
        self.__decoratorsXML = ""

    def addLine(self, point0, point1, blockType):
        """
        Add a line of a specific block type from point0 to point1, where each point is specified as an (x, y, z) tuple relative to the origin (0, 0, 0).
        """
        tPoint0 = translatePoint(self.__origin, point0)
        tPoint1 = translatePoint(self.__origin, point1)
        self.__decoratorsXML += '''<DrawLine x1="{}" y1="{}" z1="{}" x2="{}" y2="{}" z2="{}" type="{}"/>'''.format(tPoint0[0], tPoint0[1], tPoint0[2], tPoint1[0], tPoint1[1], tPoint1[2], blockType.value)

    def addSphere(self, center, radius, blockType):
        """
        Add a sphere of a specific block type, with a given radius and center relative to origin (0, 0, 0).
        """
        tCenter = translatePoint(self.__origin, center)
        self.__decoratorsXML += '''<DrawSphere x="{}" y="{}" z="{}" radius="{}" type="{}"/>'''.format(tCenter[0], tCenter[1], tCenter[2], radius, blockType.value)

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

    def __init__(self, name, startPosition):
        self.name = name
        self.position = startPosition  # (x, y, z)
        self.__inventoryXML = ""
        self.__handlersXML = ""

    def finish(self):
        """
        Returns the complete XML string for this agent being built.
        """
        return '''
        <AgentSection mode="Survival">
        <Name>{}</Name>
        <AgentStart>
            <Placement x="{}" y="{}" z="{}" yaw="0"/>
            <Inventory>{}</Inventory>
        </AgentStart>
        <AgentHandlers>{}</AgentHandlers>
        </AgentSection>'''.format(self.name, str(self.position[0]), str(self.position[1]), str(self.position[2]), self.__inventoryXML, self.__handlersXML)


class ScenarioBuilder:
    """
    Builder for creating a scenario in the form of a new Malmo mission. All added decorators are relative to
    the origin provided, which is represented as a tuple containing the following: (x, y, z).
    The origin marks the player-agent starting position and should not be changed.
    """

    def __init__(self, description, timeLimit, origin):
        # TODO: Change this to account for both player agent AND companion agent
        self.description = description
        self.timeLimit = timeLimit
        self.__origin = origin    # (x, y, z)
        self.decorations = DecorationBuilder(origin)
        self.playerAgent = AgentBuilder("PlayerAgent", origin)

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
            </Mission>'''.format(self.description, self.decorations.finish(), str(self.timeLimit), self.playerAgent.finish())