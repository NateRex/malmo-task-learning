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
    PLAN_UPDATE_COUNTER = 5000

    def __init__(self, name, generate_new_plan):
        super(HTNAgent, self).__init__(name)
        self.generate_new_plan = generate_new_plan     # A function pointer to the plan generator for this mission in particular
        self.plan = []                                 # A list of string actions returned by each call to the HTN
        self.__planCounter__ = 1                       # A counter that is incremented in each iteration of the mission loop, determining when to generate a new plan

    def __mapPlanTupleToAction__(self, planTuple):
        """
        Given an action to perform as a string, select the appropriate agent function to perform and return it
        along with any parameters in a tuple object. Returns None if the action could not be resolved.
        """
        if len(planTuple) == 3:    # COMMANDS LOGGED W/ 2 ARGUMENTS ==================================================
            if planTuple[0] == "ATTACK":
                entityType = "".join([i for i in planTuple[2] if not i.isdigit()]).capitalize()
                if isMob(entityType):
                    mobId = planTuple[2].capitalize()
                    mob = self.getNearbyEntityById(mobId)
                    if mob != None:
                        return Action(self.attackMob, [mob])
                return None
            elif planTuple[0] == "CRAFT":
                ### TODO: In the log, we only output that we crafted an item, and do not include the recipe
                ### Therefore, we do not know the recipe of items to pass to the craft function in order to craft the item given.
                return None
        elif len(planTuple) == 4:  # COMMANDS LOGGED W/ 3 ARGUMENTS =======================================================
            if planTuple[0] == "LOOKAT":
                # There are several versions of the lookAt command, depending on the type of entity
                entityType = "".join([i for i in planTuple[3] if not i.isdigit()]).capitalize()
                if isMob(entityType) or isItem(entityType):
                    entityId = planTuple[3].capitalize()
                    entity = self.getNearbyEntityById(entityId)
                    if entity != None:
                        return Action(self.lookAtEntity, [entity])
                else:
                    agentId = planTuple[3].capitalize()
                    agent = self.getNearbyEntityById(agentId)
                    if agent != None:
                        return Action(self.lookAtAgent, [agent])
                return None
            elif planTuple[0] == "MOVETO":
                # There are several versions of the moveTo command, depending on the type of entity
                entityType = "".join([i for i in planTuple[3] if not i.isdigit()]).capitalize()
                if isMob(entityType):
                    mobId = planTuple[3].capitalize()
                    mob = self.getNearbyEntityById(mobId)
                    if mob != None:
                        return Action(self.moveToMob, [mob])
                elif isItem(entityType):
                    itemId = planTuple[3].capitalize()
                    item = self.getNearbyEntityById(itemId)
                    if item != None:
                        return Action(self.__moveToItem__, [item])
                else:
                    agentId = planTuple[3].capitalize()
                    agent = HTNAgent.findAgentById(agentId)
                    if agent != None:
                        return Action(self.moveToAgent, [agent])
                return None
            elif planTuple[0] == "GIVEITEM":
                itemType = "".join([i for i in planTuple[2] if not i.isdigit()]).capitalize()
                if isItem(itemType):
                    item = self.inventory.itemById(planTuple[2])
                    receivingAgent = Agent.findAgentById(planTuple[3])
                    if item != None and receivingAgent != None:
                        return Action(self.giveItemToAgent, [item, receivingAgent])
                return None
        return None

    def __updatePlan__(self):
        """
        Update the action plan for this agent by feeding the current state of this environment to the trained HTN.
        """
        currentState = Logger.getCurrentState(HTNAgent.agentList)
        print("========================= CURRENT STATE =========================")
        print(currentState)
        newPlanTuples = self.generate_new_plan(currentState)
        print("========================= PLAN =========================")
        print(newPlanTuples)

        if newPlanTuples == None:
            return

        self.plan = []
        for planTuple in newPlanTuples:
            action = self.__mapPlanTupleToAction__(planTuple)
            if action != None:
                self.plan.append(action)

    def performNextAction(self):
        """
        Given the current environment and the trained HTN, perform the next action in the plan.
        """
        # If we have made 100 iterations of the mission loop, re-generate the plan automatically using the HTN
        # This is so that if we need to repeat an action that was previously deleted from the plan, it will reappear during a reoccurring refresh
        if self.__planCounter__ >= HTNAgent.PLAN_UPDATE_COUNTER:
            self.__updatePlan__()
            self.__planCounter__ = 0
        self.__planCounter__ += 1

        # If there are no actions to perform, do nothing
        if len(self.plan) == 0:
            return

        # Go through the list of actions, performing each and immediately moving onto the next one if it returns true
        # If the action returns false, it either failed or is not finished. Return and wait until the next iteration to try again.
        for action in self.plan:
            # Update the arguments of this function (particularly if they include entities with x,y,z positions)
            for i in range(0, len(action.args)):
                if isEntityInfoNamedTuple(action.args[i]):
                    updatedEntity = self.getNearbyEntityById(action.args[i].id)
                    if updatedEntity != None:
                        action.args[i] = updatedEntity
                    else:
                        self.__planCounter__ = HTNAgent.PLAN_UPDATE_COUNTER
                        return
            
            if not action.function(*action.args):
                return