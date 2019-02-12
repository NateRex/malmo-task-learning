import random
import mytreehop as treehop
from copy import deepcopy
# see minecraft_plan_generator.ipynb

types = ["companion", "player", "zombie", "dead", "alive"]
constants = ["none", "nonetype"]


def ATTACK(state, actor, target):

    # actor must be an agent, so that it is in
    # state.agent_looking_at[actor] and state.agent_looking_at[actor]
    if not actor in state.agents:
        return False
    if not state.agent_looking_at[actor] == target:
        return False
    if not state.agent_at[actor] == target:
        return False
    # only living things can attack living things
    if not state.status[actor] == "alive":
        return False
    if not state.status[target] == "alive":
        return False
    # don't allow attacking anything that is not a mob
    # but the mob's type doesn't matter
    if not target in state.mobs:
        return False

    preconds = {"agent_looking_at": {actor: target},
               "agent_at": {actor: target},
               "agents": {actor: state.agents[actor]},
               "mobs": {target: state.mobs[target]},
               "status": {actor:"alive", target:"alive"}
              }

    successful_state = deepcopy(state)
    successful_state.status[target] = "dead"

    return [successful_state, state], preconds


def MOVETO(state, actor, current, target):

    # we need to enforce that actor is in agents
    # so that we can know how to look up what actor is looking at
    # if instead of "agent_looking_at" we just had "looking_at" as the atom type
    # we would not need include the agents subdict in preconds
    if not hasattr(state, "agents"): # this must exist so that actor is typed
           return False
    if actor not in state.agents:
        return False
    # actor must be at current
    if not hasattr(state, "agent_at"):
        return False
    if state.agent_at[actor] != current:
        return False
    # actor must be looking at target
    if state.agent_looking_at[actor] != target:
        return False

    preconds = {"agents": {actor: state.agents[actor]},
                "agent_looking_at": {actor: target},
                "status": {actor:"alive", target:"alive"},
                "agent_at": {actor: current}
               }

    successful_state = deepcopy(state)
    successful_state.agent_at[actor] = target

    return [successful_state, state], preconds

def LOOKAT(state, actor, current, target):

    # PRECOND 1
    # we need to enforce that actor is in agents
    # so that we can know how to look up what actor is looking at
    # if instead of "agent_looking_at" we just had "looking_at" as the atom type
    # we would not need include the agents subdict in preconds
    if not hasattr(state, "agents"): # this must exist so that actor is typed
        #raise Exception()
        return False
    if not actor in state.agents:
        #raise Exception()
        return False
    # PRECOND 2
    # actor must be looking at expected current
    if not(state.agent_looking_at[actor] == current):
        #raise Exception()
        return False
    # PRECOND 3
    # only living actors can turn to look at living targets
    # an actor can only be looking at a dead target if
    # the actor was looking at that target before the target died
    if not(state.status[actor] == "alive" or state.status[target] == "alive"):
        raise Exception()
        return False

    # we don't need to guarantee the type of target or current
    # because its not necessary to know them
    # to make the necessary change to agent_looking_at[actor]
    # (not sure about this)
    preconds = {"agents": {actor: state.agents[actor]}, # PRECOND 1
                "agent_looking_at": {actor: current}, # PRECOND 2
               "status": {actor: 'alive', target: 'alive'} # PRECOND 3
               }

    successful_state = deepcopy(state)
    successful_state.agent_looking_at[actor] = target

    return [successful_state, state], preconds


ops = [ATTACK, LOOKAT, MOVETO]
treehop.declare_operators(*ops)

# if __name__ == "__main__":
    # test the preconds
