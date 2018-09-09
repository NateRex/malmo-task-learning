# ==============================================================================================
# This file contains functionality for building up a scenario to be ran as a Malmo Python
# mission. Note: The only class in this file that should be used directly by callers is the
# ScenarioBuilder
# ==============================================================================================

# Internal class used by ScenarioBuilder for developing the XML for the environment an agent will act in
class DecorationBuilder:

    # Begin a builder for a new set of decorations
    def __init__(self):
        self.generatorString = "3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"
        self.decoratorsXML = ""

    # Return the complete XML string for this set of decorations
    def finish(self):
        return '''
        <FlatWorldGenerator generatorString="''' + self.generatorString + '''"/>
        <DrawingDecorator>
        ''' + self.decoratorsXML + '''
        </DrawingDecorator>
        '''
    

# Internal class used by ScenarioBuilder for developing the XML for an agent in a Malmo mission
class AgentBuilder:

    # Begin a builder for a new agent of a specific name
    def __init__(self, name):
        self.name = name
        self.position = (0.5, 56, 0.5, 0)  # (x, y, z, yaw)
        self.inventoryXML = ""
        self.handlersXML = ""

    # Return the complete XML string for this agent being built
    def finish(self):
        return '''
        <AgentSection mode="Survival">
        <Name>''' + self.name + '''</Name>
        <AgentStart>
            <Placement x="''' + self.position[0] + '''" y="''' + self.position[1] + '''" z="''' + self.position[2] + '''" yaw="''' + self.position[3] + '''"/>
            <Inventory>
                ''' + self.inventoryXML + '''
            </Inventory>
        </AgentStart>
        <AgentHandlers>''' + self.handlersXML + '''</AgentHandlers>
        </AgentSection>'''


# Builder for creating a scenario for a new Malmo mission
# One of the first actions that should be taken by the caller is to set the player
# agent's starting position, since all other added decorators are relative to this
# position
class ScenarioBuilder:

    # Begin a builder for a new player/companion scenario in a Malmo mission using a
    # description for the scenario and a time limit
    def __init__(self, description, timeLimit):
        # TODO: Change this to account for both player agent AND companion agent
        self.description = description
        self.timeLimit = timeLimit
        self.decorations = DecorationBuilder()
        self.playerAgent = AgentBuilder("PlayerAgent")

    # Returns the complete XML string for the current scenario
    def finish(self):
        return '''
        <?xml version="1.0" encoding="UTF-8" standalone="no" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <About>
                <Summary>''' + self.description + '''</Summary>
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
                        ''' + self.decorations.finish() + '''
                        <ServerQuitFromTimeUp timeLimitMs="''' + self.timeLimit + '''"/>
                    <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
            </ServerSection>
            
            ''' + self.playerAgent.finish() + '''</Mission>'''