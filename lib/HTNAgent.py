# ==============================================================================================
# This file contains code for the HTNAgent class, representing an Agent that interfaces with
# a trained HTN in order to select actions based on the current environment state.
# ==============================================================================================
from Agent import *

class HTNAgent(Agent):
    """
    Wrapper class for a Malmo agent that interfaces with a trained hierarchical task network
    in order to select actions based on the current state.
    """

    def __init__(self, name):
        super(HTNAgent, self).__init__(name)
        self.plan = []                  # A list of string actions returned by each call to the HTN
        self.__planCounter__ = 1        # A counter that is incremented in each iteration of the mission loop, determining when to generate a new plan

    def __mapStringToFunction__(self, actionStr):
        """
        Given an action to perform as a string, select the appropriate agent function to perform and return it
        along with any parameters in a tuple object. Returns None if the action could not be resolved.
        """
        tokens = actionStr.split("-")

        if len(tokens) == 3:    # COMMANDS LOGGED W/ 2 ARGUMENTS ==================================================
            if tokens[0] == "!LOOKAT":
                # There are several versions of the lookAt command, depending on the type of entity
                entityType = "".join([i for i in tokens[2] if not i.isdigit()])
                if isMob(entityType) or isItem(entityType):
                    entity = self.getNearbyEntityById(tokens[2])
                    if entity != None:
                        return Action(self.lookAtEntity, [entity])
                else:
                    agent = HTNAgent.findAgentById(tokens[2])
                    if agent != None:
                        return Action(self.lookAtAgent, [agent])
                return None
            elif tokens[0] == "!MOVETO":
                # There are several versions of the moveTo command, depending on the type of entity
                entityType = "".join([i for i in tokens[2] if not i.isdigit()])
                if isMob(entityType):
                    mob = self.getNearbyEntityById(tokens[2])
                    if mob != None:
                        return Action(self.moveToMob, [mob])
                elif isItem(entityType):
                    item = self.getNearbyEntityById(tokens[2])
                    if item != None:
                        return Action(self.moveToItem, [item])
                else:
                    agent = HTNAgent.findAgentById(tokens[2])
                    if agent != None:
                        return Action(self.moveToAgent, [agent])
                return None
            elif tokens[0] == "!ATTACK":
                entityType = "".join([i for i in tokens[2] if not i.isdigit()])
                if isMob(entityType):
                    mob = self.getNearbyEntityById(tokens[2])
                    if mob != None:
                        return Action(self.attackMob, [entity])
                return None
            elif tokens[0] == "!CRAFT":
                ### TODO: In the log, we only output that we crafted an item, and do not include the recipe
                ### Therefore, we do not know the recipe of items to pass to the craft function in order to craft the item given.
                return None
        elif len(tokens) == 4:  # COMMANDS LOGGED W/ 3 ARGUMENTS =======================================================
            if tokens[0] == "!GIVEITEM":
                itemType = "".join([i for i in tokens[2] if not i.isdigit()])
                if isItem(itemType):
                    item = self.inventory.itemById(self, tokens[2])
                    receivingAgent = Agent.findAgentById(tokens[3])
                    if item != None and receivingAgent != None:
                        return Action(self.giveItemToAgent, [item, receivingAgent])
                return None
        return None

    def updatePlan(self):
        """
        Update the action plan for this agent by feeding the current state of this environment to the trained HTN.
        """
        currentState = Logger.getCurrentState(HTNAgent.agentList)
        # TODO
        self.plan = []

    def performNextAction(self):
        """
        Given the current environment and the trained HTN, perform the next action in the plan.
        """
        # If we have made 100 iterations of the mission loop, re-generate the plan automatically using the HTN
        # This is so that if we need to repeat an action that was previously deleted from the plan, it will reappear during a reoccurring refresh
        if self.__planCounter__ == 100:
            self.updatePlan()
            self.__planCounter__ = 0
        self.__planCounter__ += 1

        # If there are no actions to perform, do nothing
        if len(self.plan) == 0:
            return

        # Get the action to perform
        actionToPerform = self.__mapStringToFunction__(self.plan[0])
        if actionToPerform == None:
            del self.plan[0]
            return

        # Perform the action
        didSucceed = actionToPerform.function(*actionToPerform.args)
        if didSucceed:
            del self.plan[0]
