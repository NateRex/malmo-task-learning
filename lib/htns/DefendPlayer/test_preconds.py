from preconds import *
from pprint import pprint

actor = "actor"
target = "target"
current = "current"

def test_moveto_preconditions():

    state = {"agents": {actor: "companion"}, # PRECOND 1
                "agent_looking_at": {actor: target}, # PRECOND 3
                "status": {actor: alive, target: alive}, # PRECOND 4 & 5
                "agent_at": {actor: current} # PRECOND 2
             }

    result = moveto_preconds(state, actor, current, target)
    assert len(result) == 2
    preconds_met, preconds_dict = result
    assert preconds_met
    assert preconds_dict == state

    # # test that we will actually fail if those conditions aren't met
    # state = {"agents": {actor: actor}, # PRECOND 1
    #             "agent_looking_at": {actor: target}, # PRECOND 3
    #             "status": {actor: alive, target: target_status}, # PRECOND 4 & 5
    #             "agent_at": {actor: current} # PRECOND 2
    #          }

def test_attack_preconditions():
    state = {"agent_looking_at": {actor: target}, # PRECOND 2
               "agent_at": {actor: target},          # PRECOND 3
               "agents": {actor: companion}, # PRECOND 1
               "mobs": {target: zombie}, # PRECOND 5
               "status": {actor: alive, target: alive} # PRECOND 4
              }
    result = attack_preconds(state, actor, target)
    assert len(result) == 2
    preconds_met, preconds_dict = result
    assert preconds_met
    assert preconds_dict == state


def test_lookat_preconditions():
    state = {"agents": {actor: companion}, # PRECOND 1
                "agent_looking_at": {actor: current}, # PRECOND 2
               "status": {actor: alive, target: alive} # PRECOND 3
               }
    result = lookat_preconds(state, actor, current, target)
    assert len(result) == 2
    preconds_met, preconds_dict = result
    assert preconds_met
    assert preconds_dict == state

    victim = "victim"
    state = {"agents": {actor: companion, victim: player}, # PRECOND 1
            "agent_looking_at": {actor: current}, # PRECOND 2
           "status": {actor: alive, target: alive, victim: alive}, # PRECOND 3
           "closest_hostile_mob": {victim :target}
           }

    result = lookat_preconds(state, actor, current, target)
    assert len(result) == 2
    preconds_met, preconds_dict = result
    assert preconds_met
    pprint (preconds_dict)
    assert preconds_dict == state
