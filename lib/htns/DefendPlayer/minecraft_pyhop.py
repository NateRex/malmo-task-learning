from copy import deepcopy
from functools import partial
import pyhop as planner

# preconds contains definitions of types and constants,
# as well as functions which test whether state meets the operators preconds
# and return either False, (True, preconds_dict), or (data, preconds_dict)
from preconds import *

def ATTACK(state, actor, target):

    preconds_met = attack_preconds(vars(state), actor, target)
    if not preconds_met:
        return preconds_met

    successful_state = deepcopy(state)
    successful_state.status[target] = dead
    return successful_state

def MOVETO(state, actor, current, target):
    preconds_met = moveto_preconds(vars(state), actor, current, target)
    if not preconds_met:
        return preconds_met

    successful_state = deepcopy(state)
    successful_state.agent_at[actor] = target
    return successful_state

def LOOKAT(state, actor, current, target):
    preconds_met = lookat_preconds(vars(state), actor, current, target)
    if not preconds_met:
        return preconds_met

    successful_state = deepcopy(state)
    successful_state.agent_looking_at[actor] = target
    return successful_state

ops = [ATTACK, LOOKAT, MOVETO]
planner.declare_operators(*ops)
