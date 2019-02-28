from copy import deepcopy
from functools import partial
import mytreehop as planner

# preconds contains definitions of types and constants,
# as well as functions which test whether state meets the operators preconds
# and return either False, (True, preconds_dict), or (data, preconds_dict)
from preconds import * # defines dead = "dead", player = "player", etc

def ATTACK(state, actor, target):
    results = action_preconds(state, actor, target)
    if not results:
        return results
    preconds_met, preconds_dict = results

    successful_state = deepcopy(state)
    successful_state.status[target] = dead

    return [successful_state, state], preconds_dict


def MOVETO(state, actor, current, target):
    results = moveto_preconds(state, actor, current, target)
    if not results:
        return results
    preconds_met, preconds_dict = results

    successful_state = deepcopy(state)
    successful_state.agent_at[actor] = target

    return [successful_state, state], preconds

def LOOKAT(state, actor, current, target):
    results = lookat_preconds(state, actor, current, target)
    if not results:
        return results
    preconds_met, preconds_dict = results

    successful_state = deepcopy(state)
    successful_state.agent_looking_at[actor] = target

    return [successful_state, state], preconds_dict

# def LOOKAT(state, actor, current, target):
#
#     # PRECOND 1
#     # we need to enforce that actor is in agents
#     # so that we can know how to look up what actor is looking at
#     # if instead of "agent_looking_at" we just had "looking_at" as the atom type
#     # we would not need include the agents subdict in preconds
#     if not hasattr(state, "agents"): # this must exist so that actor is typed
#         #raise Exception()
#         return False
#     if not actor in state.agents:
#         #raise Exception()
#         return False
#     # PRECOND 2
#     # actor must be looking at expected current
#     if not(state.agent_looking_at[actor] == current):
#         #raise Exception()
#         return False
#     # PRECOND 3
#     # only living actors can turn to look at non-dead targets
#     # an actor can only be looking at a dead target if
#     # the actor was looking at that target before the target died
#
#     if not(state.status[actor] == alive or state.status[target] == alive):
#         raise Exception()
#         return False
#
#     # we don't need to guarantee the type of target or current
#     # because its not necessary to know them
#     # to make the necessary change to agent_looking_at[actor]
#     # (not sure about this)
#     preconds = {"agents": {actor: state.agents[actor]}, # PRECOND 1
#                 "agent_looking_at": {actor: current}, # PRECOND 2
#                "status": {actor: alive, target: alive} # PRECOND 3
#                }
#
#     successful_state = deepcopy(state)
#     successful_state.agent_looking_at[actor] = target
#
#     return [successful_state, state], preconds


ops = [ATTACK, LOOKAT, MOVETO]
planner.declare_operators(*ops)

# if __name__ == "__main__":
    # test the preconds
