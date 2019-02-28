"""
Helper functions for actions.
Functions should test action preconditions, returning False if preconds not met,
returning (data, preconds_dict) if preconds met, where data is either True or
any data that was calculated during the function that the operator might need.

The purpose of these functions is to provide common functions that can be used
by operator functions for either pyhop or treehop operators.

NOTE: all functions take a state dict, which you can get by calling vars(state)
on a Treehop or Pyhop state.

a TREEHOP operator would be:
```
def OP(state, *args):
    preconds_met, preconds_dict = op_preconds(vars(state), *args)

    # calculate n potential resulting states
    successful_state_i = deepcopy(state)
    # any updates that need to be made to successful_state_i

    return (successful_state_1, ..., successful_state_n), preconds_dict
```

while the PYHOP operator would be:
```
def OP(state, *args):
    preconds_met, preconds_dict = op_preconds(vars(state), *args)

    successful_state = deepcopy(state)
    # any updates that need to be made to successful_state

    return successful_state
```
"""

types = ["companion", "player", "zombie", "dead", "alive"]
constants = ["none", "nonetype"] # 'none' won't conflict with keyword 'None'
for t in types + constants:
    globals()[t] = t

def attack_preconds(state, actor, target):

    # PRECOND 1
    # actor must be an agent, so that it is in
    # state["agent_looking_at"][actor] and state["agent_looking_at"][actor]
    if not actor in state["agents"]:
        return False
    # PRECOND 2
    if not state["agent_looking_at"][actor] == target:
        return False
    # PRECOND 3
    if not state["agent_at"][actor] == target:
        return False
    # PRECOND 4
    # only living things can attack living things
    if not state["status"][actor] == alive:
        return False
    if not state["status"][target] == alive:
        return False
    # PRECOND 5
    # don't allow attacking anything that is not a mob
    # but the mob's type doesn't matter
    if not target in state["mobs"]:
        return False

    preconds = {"agent_looking_at": {actor: target}, # PRECOND 2
               "agent_at": {actor: target},          # PRECOND 3
               "agents": {actor: state["agents"][actor]}, # PRECOND 1
               "mobs": {target: state["mobs"][target]}, # PRECOND 5
               "status": {actor: alive, target: alive} # PRECOND 4
              }

    return True, preconds

def moveto_preconds(state, actor, current, target):

    # PRECOND 1
    # we need to enforce that actor is in agents
    # so that we can know how to look up what actor is looking at
    # if instead of "agent_looking_at" we just had "looking_at" as the atom type
    # we would not need include the agents subdict in preconds
    if "agents" not in state: # this must exist so that actor is typed
        return False
    if actor not in state["agents"]:
        return False
    # PRECOND 2
    # actor must be at current
    if "agent_at" not in state:
        return False
    if state["agent_at"][actor] != current:
        return False
    # PRECOND 3
    # actor must be looking at target
    if state["agent_looking_at"][actor] != target:
        return False

    # preconds regarding status of actor and target
    # should something with no entry in status is reachable or not?

    # PRECOND 4
    # actor must be alive to move
    if ("status" not in state
        or actor not in state["status"]
        or state["status"][actor] != alive):
        return False
    # PRECOND 5
    # target must not be dead (or any other status category that means 'not reachable')
    # it must be in the status dict
    if target not in state["status"] or state["status"][target] == dead:
        return False
    target_status = state["status"][target]

    preconds = {"agents": {actor: state["agents"][actor]}, # PRECOND 1
                "agent_looking_at": {actor: target}, # PRECOND 3
                "status": {actor: alive, target: target_status}, # PRECOND 4 & 5
                "agent_at": {actor: current} # PRECOND 2
               }

    return True, preconds


def lookat_preconds(state, actor, current, target):
    """
    If state does not meet the preconditions, return False
    If state does meet one of the two sets of preconditions, return a tuple of 2 lists,
        threats
        victims
    preconds:
    common:
    - actor is in agents
    - actor is looking at current
    - target is not dead

    set 1:
    - target is closest_hostile_mob for at least one agent A
    - agent A is type player and is has status alive


    set 2:
    - there are no
    """

    # PRECOND 1
    # we need to enforce that actor is in agents
    # so that we can know how to look up what actor is looking at
    # if instead of "agent_looking_at" we just had "looking_at" as the atom type
    # we would not need include the agents subdict in preconds
    if "agents" not in state: # this must exist so that actor is typed
        #raise Exception()
        return False
    if not actor in state["agents"]:
        #raise Exception()
        return False
    # PRECOND 2
    # actor must be looking at expected current
    if not(state["agent_looking_at"][actor] == current):
        #raise Exception()
        return False

    # PRECOND 4
    # if target is in closest_hostile_mob, continue
    # if closest_hostile_mob is alive and target is not closest_hostile_mob, fail
    # if closest_hostile_mob is dead, target may be any living mob (PRECOND 3)
    # (how do i determine which closest_hostile_mob I want, if there are more than 2 values?
    # I would need to know which player I am defending. Or maybe just have
    # precond that the value I choose for mob must be the closest_hostile_mob of
    # a player agent.)
    threats = []
    victims = []
    if "closest_hostile_mob" in state:
        # get only mobs that are closest hostile mob to an agent w/ type player?
        threats = []
        closest_hostile_mob = state["closest_hostile_mob"].items()
        for victim, threat in closest_hostile_mob:
            if state["agents"][victim] == player and state["status"][victim] == alive:
                threats.append(threat)

        if target not in threats:
            # if target is not a threat and
            # any threats are alive, fail
            mobs_alive = [state["status"][mob] == alive for mob in threats]
            if any(mobs_alive):
                return False
        else:
            # if target in threats, which alive player agents is it threatening?
            for victim, threat in closest_hostile_mob:
                if (threat == target
                    and state["agents"][victim] == player
                    and state["status"][victim] == alive):
                    victims.append(victim)

        # I don't know how to encode that none of the values of closest_hostile_mob
        # correspond to living mobs. I could take each (agent, closest_hostile_mob)
        # pair and include it under preconds["closest_hostile_mob"] and take each
        # closest_hostile_mob value and set preconds["status"] as alive
        # if target in closest_hostile_mob, then preconds should include
        # "closest_hostile_mob": {victim: mob}
        # "status": {mob: "alive"}

    # PRECOND 3
    # only living actors can turn to look at living targets
    # an actor can only be looking at a dead target if
    # the actor was looking at that target before the target died
    # also: target is acceptable so long as target is not dead
    # target is not in status, or target is in status and is not dead
    target_not_dead = ((target in state["status"] and state["status"][target] != dead)
                       or target not in state["status"])
    if not(state["status"][actor] == alive and target_not_dead):
        raise Exception()
        return False

    preconds = {"agents": {actor: state["agents"][actor]}, # PRECOND 1
                "agent_looking_at": {actor: current}, # PRECOND 2
               "status": {actor: alive, target: alive} # PRECOND 3
               }

    if target in threats:
        # for each of target's living victims,
        # add victim, target pair to closest_hostile_mob
        # and victim's "alive" status to status
        preconds["closest_hostile_mob"] = {}
        for v in victims:
            preconds["closest_hostile_mob"][v] = target
            preconds["status"][v] = alive
            preconds["agents"][v] = player

    return (threats, victims), preconds


if __name__ == "__main__":
    pass
