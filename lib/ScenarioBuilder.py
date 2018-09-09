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
        self.generatorString = "3;7,2*3,2;1;"
        self.decoratorsXML = ""

    # Return the complete XML string for this set of decorations
    def finish(self):
        """
        Return the complete XML string for this set of decorations
        """
        return '''
        <FlatWorldGenerator generatorString="{}"/>
        {}
        '''.format(self.generatorString, "<DrawingDecorator>" + self.decoratorsXML + "</DrawingDecorator>" if len(self.decoratorsXML) > 0 else "")
    

class AgentBuilder:
    """
    Internal class used by the ScenarioBuilder for developing XML for an agent in a Malmo mission
    """

    def __init__(self, name, startPosition):
        self.name = name
        self.position = startPosition  # (x, y, z)
        self.inventoryXML = ""
        self.handlersXML = ""

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
        </AgentSection>'''.format(self.name, str(self.position[0]), str(self.position[1]), str(self.position[2]), self.inventoryXML, self.handlersXML)


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
        self.decorations = DecorationBuilder()
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