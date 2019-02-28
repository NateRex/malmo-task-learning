# domain should import whatever version of planner (treehop or pyhop) as planner
from minecraft_pyhop import *
# from rocket_domain import *

from itertools import product
import logging
# from on_failure import output_on_failure

# planner.declare_operators(*ops)

# ###############################################################
# ####################### Learned Methods #######################
# ###############################################################



def task_lookat_companion1_none_zombie2(state, companion1, none, zombie2):

    """
    primitive

    agent_looking_at: companion1: none --> zombie2
    """


    # initialize variables
    player1 = None

    # are effects met?
    effects = ('companion1' in locals() and 'zombie2' in locals()
               and companion1 in state.agent_looking_at
               and companion1 in state.status and companion1 in state.agents
               and zombie2 == state.agent_looking_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, none, zombie2])
    if not len(params) == 3: return False

    # type check ('companion1', 'none', 'zombie2')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie2 in state.status and 'alive' == state.status[zombie2]):
    	return False

    # comparison check
    if not (none == state.agent_looking_at[companion1]): return False



    return [('LOOKAT', companion1, none, zombie2),
            ('task_lookat_companion1_none_zombie2', companion1, none, zombie2)]



def task_lookat_companion1_zombie1_zombie3(state, companion1, zombie1, zombie3):

    """
    primitive

    agent_looking_at: companion1: zombie1 --> zombie3
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie3' in locals()
               and companion1 in state.agent_looking_at
               and companion1 in state.status and companion1 in state.agents
               and zombie3 == state.agent_looking_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, zombie1, zombie3])
    if not len(params) == 3: return False

    # type check ('companion1', 'zombie1', 'zombie3')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False

    # comparison check
    if not (zombie1 == state.agent_looking_at[companion1]): return False



    return [('LOOKAT', companion1, zombie1, zombie3),
            ('task_lookat_companion1_zombie1_zombie3', companion1, zombie1,
             zombie3)]



def task_moveto_companion1_zombie2_zombie1(state, companion1, zombie2, zombie1):

    """
    primitive

    agent_at: companion1: zombie2 --> zombie1
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie1' in locals()
               and companion1 in state.agent_at and companion1 in state.status
               and companion1 in state.agents
               and zombie1 == state.agent_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2])
    if not len(params) == 3: return False

    # type check ('companion1', 'zombie1', 'zombie2')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False

    # comparison check
    if not (zombie1 == state.agent_looking_at[companion1]): return False
    if not (zombie2 == state.agent_at[companion1]): return False



    return [('MOVETO', companion1, zombie2, zombie1),
            ('task_moveto_companion1_zombie2_zombie1', companion1, zombie2,
             zombie1)]



def task_moveto_companion1_none_zombie2(state, companion1, none, zombie2):

    """
    primitive

    agent_at: companion1: none --> zombie2
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie2' in locals()
               and companion1 in state.agent_at and companion1 in state.status
               and companion1 in state.agents
               and zombie2 == state.agent_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, none, zombie2])
    if not len(params) == 3: return False

    # type check ('companion1', 'none', 'zombie2')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie2 in state.status and 'alive' == state.status[zombie2]):
    	return False

    # comparison check
    if not (none == state.agent_at[companion1]): return False
    if not (zombie2 == state.agent_looking_at[companion1]): return False



    return [('MOVETO', companion1, none, zombie2),
            ('task_moveto_companion1_none_zombie2', companion1, none, zombie2)]



def task_moveto_companion1_none_zombie3(state, companion1, none, zombie3):

    """
    primitive

    agent_at: companion1: none --> zombie3
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie3' in locals()
               and companion1 in state.agent_at and companion1 in state.status
               and companion1 in state.agents
               and zombie3 == state.agent_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, none, zombie3])
    if not len(params) == 3: return False

    # type check ('companion1', 'none', 'zombie3')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False

    # comparison check
    if not (none == state.agent_at[companion1]): return False
    if not (zombie3 == state.agent_looking_at[companion1]): return False



    return [('MOVETO', companion1, none, zombie3),
            ('task_moveto_companion1_none_zombie3', companion1, none, zombie3)]



def task_moveto_companion1_none_zombie1(state, companion1, none, zombie1):

    """
    primitive

    agent_at: companion1: none --> zombie1
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie1' in locals()
               and companion1 in state.agent_at and companion1 in state.status
               and companion1 in state.agents
               and zombie1 == state.agent_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, none, zombie1])
    if not len(params) == 3: return False

    # type check ('companion1', 'none', 'zombie1')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False

    # comparison check
    if not (none == state.agent_at[companion1]): return False
    if not (zombie1 == state.agent_looking_at[companion1]): return False



    return [('MOVETO', companion1, none, zombie1),
            ('task_moveto_companion1_none_zombie1', companion1, none, zombie1)]



def task_moveto_companion1_zombie3_zombie1(state, companion1, zombie3, zombie1):

    """
    primitive

    agent_at: companion1: zombie3 --> zombie1
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie1' in locals()
               and companion1 in state.agent_at and companion1 in state.status
               and companion1 in state.agents
               and zombie1 == state.agent_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, zombie1, zombie3])
    if not len(params) == 3: return False

    # type check ('companion1', 'zombie1', 'zombie3')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False

    # comparison check
    if not (zombie1 == state.agent_looking_at[companion1]): return False
    if not (zombie3 == state.agent_at[companion1]): return False



    return [('MOVETO', companion1, zombie3, zombie1),
            ('task_moveto_companion1_zombie3_zombie1', companion1, zombie3,
             zombie1)]



def task_moveto_companion1_zombie3_zombie2(state, companion1, zombie3, zombie2):

    """
    primitive

    agent_at: companion1: zombie3 --> zombie2
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie2' in locals()
               and companion1 in state.agent_at and companion1 in state.status
               and companion1 in state.agents
               and zombie2 == state.agent_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, zombie2, zombie3])
    if not len(params) == 3: return False

    # type check ('companion1', 'zombie3', 'zombie2')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie2 in state.status and 'alive' == state.status[zombie2]):
    	return False

    # comparison check
    if not (zombie3 == state.agent_at[companion1]): return False
    if not (zombie2 == state.agent_looking_at[companion1]): return False



    return [('MOVETO', companion1, zombie3, zombie2),
            ('task_moveto_companion1_zombie3_zombie2', companion1, zombie3,
             zombie2)]



def task_lookat_companion1_zombie2_zombie3(state, companion1, zombie2, zombie3):

    """
    primitive

    agent_looking_at: companion1: zombie2 --> zombie3
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie3' in locals()
               and companion1 in state.agent_looking_at
               and companion1 in state.status and companion1 in state.agents
               and zombie3 == state.agent_looking_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, zombie2, zombie3])
    if not len(params) == 3: return False

    # type check ('companion1', 'zombie3', 'zombie2')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False

    # comparison check
    if not (zombie2 == state.agent_looking_at[companion1]): return False



    return [('LOOKAT', companion1, zombie2, zombie3),
            ('task_lookat_companion1_zombie2_zombie3', companion1, zombie2,
             zombie3)]



def task_lookat_companion1_zombie2_player1(state, companion1, zombie2, player1):

    """
    primitive

    agent_looking_at: companion1: zombie2 --> player1
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'player1' in locals()
               and companion1 in state.agent_looking_at
               and companion1 in state.status and companion1 in state.agents
               and player1 == state.agent_looking_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, player1, zombie2])
    if not len(params) == 3: return False

    # type check ('companion1', 'player1', 'zombie2')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False

    # comparison check
    if not (zombie2 == state.agent_looking_at[companion1]): return False



    return [('LOOKAT', companion1, zombie2, player1),
            ('task_lookat_companion1_zombie2_player1', companion1, zombie2,
             player1)]



def task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie1_dead__1(state, zombie1):

    """
    basic

    status: zombie1: alive --> dead
    """


    # assignment by lookup

    # variable uniqueness check
    params = set([zombie1])
    if not len(params) == 1: return False

    # type check ('zombie1',)
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False

    # search state to assign remaining variables

    # section 0
    companion1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'companion' and p in state.agent_looking_at
        and state.agent_looking_at[p] == zombie1 and p not in params
    ]
    if not (companion1s): return False
    companion1 = companion1s[0]
    params.update([companion1])

    params = set([companion1, zombie1])

    if not len(params) == 2:
    	raise RuntimeError('searched variables are not unique.')



    return [('task_attack_companion1_zombie1', companion1, zombie1)]



def task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie1_dead__2(state, companion1, zombie1):

    """
    basic

    status:
        zombie1: alive --> dead
    agent_at:
        companion1: zombie3 --> zombie1
    agent_looking_at:
        companion1: zombie3 --> zombie1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie3])
    if not len(params) == 3: return False

    # type check ('zombie1', 'zombie3')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False



    return [('task_lookat_companion1_zombie3_zombie1', companion1, zombie3,
             zombie1), ('task_moveto_companion1_zombie3_zombie1', companion1,
                        zombie3, zombie1), ('task_attack_companion1_zombie1',
                                            companion1, zombie1)]



def task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie1_dead__3(state, companion1):

    """
    complex

    status:
        zombie1: alive --> dead
    agent_at:
        companion1: none --> zombie1
    """


    # assignment by lookup
    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie1])
    if not len(params) == 3: return False

    # type check ('none', 'zombie1')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False



    return [('task_AGENT_AT_companion1_zombie1', companion1), (
        'task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie1_dead',
        zombie1)]



def task_AGENT_LOOKING_AT_companion1_zombie1__1(state, companion1, zombie1):

    """
    basic

    agent_looking_at: companion1: none --> zombie1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie1])
    if not len(params) == 3: return False

    # type check ('none', 'zombie1')
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False

    ('status', 'alive')
    ('agents', 'player')
    # search state to assign remaining variables

    # section 0
    player1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'player' and p in state.closest_hostile_mob
        and state.closest_hostile_mob[p] == zombie1 and p not in params
    ]
    if not (player1s): return False
    player1 = player1s[0]
    params.update([player1])

    params = set([companion1, none, player1, zombie1])

    if not len(params) == 4:
    	raise RuntimeError('searched variables are not unique.')



    return [('task_lookat_companion1_none_zombie1', companion1, none, zombie1)]



def task_AGENT_LOOKING_AT_companion1_zombie1__2(state, companion1, zombie1):

    """
    basic

    agent_looking_at: companion1: zombie3 --> zombie1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie3])
    if not len(params) == 3: return False

    # type check ('zombie1', 'zombie3')
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False



    return [('task_lookat_companion1_zombie3_zombie1', companion1, zombie3,
             zombie1)]



def task_AGENT_LOOKING_AT_companion1_zombie1__3(state, companion1, zombie1):

    """
    basic

    agent_looking_at: companion1: zombie2 --> zombie1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2])
    if not len(params) == 3: return False

    # type check ('zombie1', 'zombie2')
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False



    return [('task_lookat_companion1_zombie2_zombie1', companion1, zombie2,
             zombie1)]



def task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie3_dead(state, companion1, zombie2, zombie3):

    """
    complex

    status:
        zombie3: alive --> dead
    agent_at:
        companion1: none --> zombie3
    agent_looking_at:
        companion1: none --> zombie2
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie2, zombie3])
    if not len(params) == 4: return False

    # type check ('none', 'zombie3', 'zombie2')
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False
    if not (zombie2 in state.status and 'alive' == state.status[zombie2]):
    	return False

    ('status', 'alive')
    ('agents', 'player')
    # search state to assign remaining variables

    # section 0
    player1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'player' and p in state.closest_hostile_mob
        and state.closest_hostile_mob[p] == zombie3 and p not in params
    ]
    if not (player1s): return False
    player1 = player1s[0]
    params.update([player1])

    params = set([companion1, none, player1, zombie3, zombie2])

    if not len(params) == 5:
    	raise RuntimeError('searched variables are not unique.')



    return [(
        'task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie3_dead',
        companion1, zombie3), ('task_AGENT_LOOKING_AT_companion1_zombie2',
                               companion1, zombie2)]



def task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie3_dead(state, companion1, zombie1):

    """
    complex

    status:
        zombie3: alive --> dead
    agent_at:
        companion1: zombie2 --> zombie1
    agent_looking_at:
        companion1: zombie3 --> zombie1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2, zombie3])
    if not len(params) == 4: return False

    # type check ('zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False



    return [(
        'task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie3_dead',
        companion1, zombie1), ('task_AGENT_AT_companion1_zombie1', companion1)]



def task_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead(state, companion1, player1):

    """
    complex

    status:
        zombie1: alive --> dead
    agent_looking_at:
        companion1: zombie1 --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, player1, zombie1])
    if not len(params) == 3: return False

    # type check ('player1', 'zombie1')
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False



    return [(
        'task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie1_dead',
        zombie1), ('task_AGENT_LOOKING_AT_companion1_player1', companion1,
                   player1)]



def task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead_zombie2_dead_zombie3_dead(state, companion1, zombie1, zombie2, zombie3):

    """
    complex

    status:
        zombie1: alive --> dead
        zombie3: alive --> dead
        zombie2: alive --> dead
    agent_at:
        companion1: none --> zombie2
    agent_looking_at:
        companion1: none --> zombie2
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie1, zombie2, zombie3])
    if not len(params) == 5: return False

    # type check ('none', 'zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False

    ('status', 'alive')
    ('agents', 'player')
    # search state to assign remaining variables

    # section 0
    player1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'player' and p in state.closest_hostile_mob
        and state.closest_hostile_mob[p] == zombie3 and p not in params
    ]
    if not (player1s): return False
    player1 = player1s[0]
    params.update([player1])

    params = set([none, companion1, player1, zombie1, zombie3, zombie2])

    if not len(params) == 6:
    	raise RuntimeError('searched variables are not unique.')



    return [(
        'task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead_zombie3_dead',
        companion1, zombie1, zombie2, zombie3),
            ('task_AGENT_AT_companion1_zombie2_STATUS_zombie2_dead', companion1)]



def task_lookat_companion1_zombie3_zombie1(state, companion1, zombie3, zombie1):

    """
    primitive

    agent_looking_at: companion1: zombie3 --> zombie1
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie1' in locals()
               and companion1 in state.agent_looking_at
               and companion1 in state.status and companion1 in state.agents
               and zombie1 == state.agent_looking_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, zombie1, zombie3])
    if not len(params) == 3: return False

    # type check ('companion1', 'zombie1', 'zombie3')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False

    # comparison check
    if not (zombie3 == state.agent_looking_at[companion1]): return False



    return [('LOOKAT', companion1, zombie3, zombie1),
            ('task_lookat_companion1_zombie3_zombie1', companion1, zombie3,
             zombie1)]



def task_attack_companion1_zombie2(state, companion1, zombie2):

    """
    primitive

    status: zombie2: alive --> dead
    """


    # initialize variables

    # assignment by lookup
    # are effects met?
    effects = ('zombie2' in locals() and zombie2 in state.mobs
               and zombie2 in state.status and dead == state.status[zombie2]
               and 'zombie' == state.mobs[zombie2])
    if effects: return []

    # variable uniqueness check
    params = set([companion1, zombie2])
    if not len(params) == 2: return False

    # type check ('companion1', 'zombie2')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False

    # comparison check
    if not (zombie2 == state.agent_looking_at[companion1]): return False



    return [('ATTACK', companion1, zombie2), ('task_attack_companion1_zombie2',
                                              companion1, zombie2)]



def task_attack_companion1_zombie3(state, companion1, zombie3):

    """
    primitive

    status: zombie3: alive --> dead
    """


    # initialize variables

    # assignment by lookup
    # are effects met?
    effects = ('zombie3' in locals() and zombie3 in state.status
               and zombie3 in state.mobs and dead == state.status[zombie3]
               and 'zombie' == state.mobs[zombie3])
    if effects: return []

    # variable uniqueness check
    params = set([companion1, zombie3])
    if not len(params) == 2: return False

    # type check ('companion1', 'zombie3')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False

    # comparison check
    if not (zombie3 == state.agent_looking_at[companion1]): return False



    return [('ATTACK', companion1, zombie3), ('task_attack_companion1_zombie3',
                                              companion1, zombie3)]



def task_lookat_companion1_zombie1_player1(state, companion1, zombie1, player1):

    """
    primitive

    agent_looking_at: companion1: zombie1 --> player1
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'player1' in locals()
               and companion1 in state.agent_looking_at
               and companion1 in state.status and companion1 in state.agents
               and player1 == state.agent_looking_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, player1, zombie1])
    if not len(params) == 3: return False

    # type check ('companion1', 'player1', 'zombie1')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False

    # comparison check
    if not (zombie1 == state.agent_looking_at[companion1]): return False



    return [('LOOKAT', companion1, zombie1, player1),
            ('task_lookat_companion1_zombie1_player1', companion1, zombie1,
             player1)]



def task_lookat_companion1_zombie1_zombie2(state, companion1, zombie1, zombie2):

    """
    primitive

    agent_looking_at: companion1: zombie1 --> zombie2
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie2' in locals()
               and companion1 in state.agent_looking_at
               and companion1 in state.status and companion1 in state.agents
               and zombie2 == state.agent_looking_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2])
    if not len(params) == 3: return False

    # type check ('companion1', 'zombie1', 'zombie2')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie2 in state.status and 'alive' == state.status[zombie2]):
    	return False

    # comparison check
    if not (zombie1 == state.agent_looking_at[companion1]): return False



    return [('LOOKAT', companion1, zombie1, zombie2),
            ('task_lookat_companion1_zombie1_zombie2', companion1, zombie1,
             zombie2)]



def task_moveto_companion1_zombie1_zombie2(state, companion1, zombie1, zombie2):

    """
    primitive

    agent_at: companion1: zombie1 --> zombie2
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie2' in locals()
               and companion1 in state.agent_at and companion1 in state.status
               and companion1 in state.agents
               and zombie2 == state.agent_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2])
    if not len(params) == 3: return False

    # type check ('companion1', 'zombie1', 'zombie2')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie2 in state.status and 'alive' == state.status[zombie2]):
    	return False

    # comparison check
    if not (zombie1 == state.agent_at[companion1]): return False
    if not (zombie2 == state.agent_looking_at[companion1]): return False



    return [('MOVETO', companion1, zombie1, zombie2),
            ('task_moveto_companion1_zombie1_zombie2', companion1, zombie1,
             zombie2)]



def task_moveto_companion1_zombie1_zombie3(state, companion1, zombie1, zombie3):

    """
    primitive

    agent_at: companion1: zombie1 --> zombie3
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie3' in locals()
               and companion1 in state.agent_at and companion1 in state.status
               and companion1 in state.agents
               and zombie3 == state.agent_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, zombie1, zombie3])
    if not len(params) == 3: return False

    # type check ('companion1', 'zombie1', 'zombie3')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False

    # comparison check
    if not (zombie1 == state.agent_at[companion1]): return False
    if not (zombie3 == state.agent_looking_at[companion1]): return False



    return [('MOVETO', companion1, zombie1, zombie3),
            ('task_moveto_companion1_zombie1_zombie3', companion1, zombie1,
             zombie3)]



def task_attack_companion1_zombie1(state, companion1, zombie1):

    """
    primitive

    status: zombie1: alive --> dead
    """


    # initialize variables

    # assignment by lookup
    # are effects met?
    effects = ('zombie1' in locals() and zombie1 in state.status
               and zombie1 in state.mobs and dead == state.status[zombie1]
               and 'zombie' == state.mobs[zombie1])
    if effects: return []

    # variable uniqueness check
    params = set([companion1, zombie1])
    if not len(params) == 2: return False

    # type check ('companion1', 'zombie1')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False

    # comparison check
    if not (zombie1 == state.agent_looking_at[companion1]): return False



    return [('ATTACK', companion1, zombie1), ('task_attack_companion1_zombie1',
                                              companion1, zombie1)]



def task_moveto_companion1_zombie3_player1(state, companion1, zombie3, player1):

    """
    primitive

    agent_at: companion1: zombie3 --> player1
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'player1' in locals()
               and companion1 in state.agent_at and companion1 in state.status
               and companion1 in state.agents
               and player1 == state.agent_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, player1, zombie3])
    if not len(params) == 3: return False

    # type check ('companion1', 'player1', 'zombie3')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False

    # comparison check
    if not (player1 == state.agent_looking_at[companion1]): return False
    if not (zombie3 == state.agent_at[companion1]): return False



    return [('MOVETO', companion1, zombie3, player1),
            ('task_moveto_companion1_zombie3_player1', companion1, zombie3,
             player1)]



def task_moveto_companion1_zombie1_player1(state, companion1, zombie1, player1):

    """
    primitive

    agent_at: companion1: zombie1 --> player1
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'player1' in locals()
               and companion1 in state.agent_at and companion1 in state.status
               and companion1 in state.agents
               and player1 == state.agent_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, player1, zombie1])
    if not len(params) == 3: return False

    # type check ('companion1', 'player1', 'zombie1')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False

    # comparison check
    if not (player1 == state.agent_looking_at[companion1]): return False
    if not (zombie1 == state.agent_at[companion1]): return False



    return [('MOVETO', companion1, zombie1, player1),
            ('task_moveto_companion1_zombie1_player1', companion1, zombie1,
             player1)]



def task_AGENT_LOOKING_AT_companion1_zombie2__1(state, companion1, zombie2):

    """
    basic

    agent_looking_at: companion1: zombie1 --> zombie2
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2])
    if not len(params) == 3: return False

    # type check ('zombie1', 'zombie2')
    if not (zombie2 in state.status and 'alive' == state.status[zombie2]):
    	return False



    return [('task_lookat_companion1_zombie1_zombie2', companion1, zombie1,
             zombie2)]



def task_AGENT_LOOKING_AT_companion1_zombie2__2(state, companion1, zombie2):

    """
    basic

    agent_looking_at: companion1: zombie3 --> zombie2
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie2, zombie3])
    if not len(params) == 3: return False

    # type check ('zombie3', 'zombie2')
    if not (zombie2 in state.status and 'alive' == state.status[zombie2]):
    	return False



    return [('task_lookat_companion1_zombie3_zombie2', companion1, zombie3,
             zombie2)]



def task_AGENT_AT_companion1_zombie3__1(state, companion1):

    """
    basic

    agent_at: companion1: zombie1 --> zombie3
    """


    # assignment by lookup
    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie3])
    if not len(params) == 3: return False

    # type check ('zombie1', 'zombie3')
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False



    return [('task_moveto_companion1_zombie1_zombie3', companion1, zombie1,
             zombie3)]



def task_AGENT_AT_companion1_zombie3__2(state, companion1):

    """
    basic

    agent_at: companion1: zombie2 --> zombie3
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie2, zombie3])
    if not len(params) == 3: return False

    # type check ('zombie3', 'zombie2')
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False



    return [('task_moveto_companion1_zombie2_zombie3', companion1, zombie2,
             zombie3)]



def task_AGENT_AT_companion1_zombie1__1(state, companion1):

    """
    basic

    agent_at: companion1: zombie2 --> zombie1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2])
    if not len(params) == 3: return False

    # type check ('zombie1', 'zombie2')
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False



    return [('task_moveto_companion1_zombie2_zombie1', companion1, zombie2,
             zombie1)]



def task_AGENT_AT_companion1_zombie1__2(state, companion1):

    """
    basic

    agent_at: companion1: none --> zombie1
    """


    # assignment by lookup
    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie1])
    if not len(params) == 3: return False

    # type check ('none', 'zombie1')
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False



    return [('task_moveto_companion1_none_zombie1', companion1, none, zombie1)]



def task_AGENT_AT_companion1_zombie1__3(state, companion1):

    """
    basic

    agent_at: companion1: zombie3 --> zombie1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie3])
    if not len(params) == 3: return False

    # type check ('zombie1', 'zombie3')
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False



    return [('task_moveto_companion1_zombie3_zombie1', companion1, zombie3,
             zombie1)]



def task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1__1(state, companion1):

    """
    basic

    agent_at: companion1: zombie1 --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	player1 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, player1, zombie1])
    if not len(params) == 3: return False

    # type check ('player1', 'zombie1')
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False



    return [('task_moveto_companion1_zombie1_player1', companion1, zombie1,
             player1)]



def task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1__2(state, companion1):

    """
    basic

    agent_at: companion1: zombie3 --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	player1 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, player1, zombie3])
    if not len(params) == 3: return False

    # type check ('player1', 'zombie3')
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False



    return [('task_moveto_companion1_zombie3_player1', companion1, zombie3,
             player1)]



def task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1__3(state, companion1, player1):

    """
    basic

    agent_at:
        companion1: zombie2 --> player1
    agent_looking_at:
        companion1: zombie2 --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, player1, zombie2])
    if not len(params) == 3: return False

    # type check ('player1', 'zombie2')
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False



    return [('task_lookat_companion1_zombie2_player1', companion1, zombie2,
             player1), ('task_moveto_companion1_zombie2_player1', companion1,
                        zombie2, player1)]



def task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie3_dead__1(state, companion1, player1):

    """
    complex

    status:
        zombie3: alive --> dead
    agent_looking_at:
        companion1: zombie3 --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, player1, zombie3])
    if not len(params) == 3: return False

    # type check ('player1', 'zombie3')
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False



    return [('task_STATUS_zombie3_dead', zombie3),
            ('task_AGENT_LOOKING_AT_companion1_player1', companion1, player1)]



def task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie3_dead__2(state, companion1, player1):

    """
    complex

    status:
        zombie3: alive --> dead
    agent_at:
        companion1: zombie2 --> zombie3
    agent_looking_at:
        companion1: zombie3 --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, player1, zombie2, zombie3])
    if not len(params) == 4: return False

    # type check ('player1', 'zombie3', 'zombie2')
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False



    return [('task_AGENT_AT_companion1_zombie3', companion1), (
        'task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie3_dead',
        companion1, player1)]



def task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead__1(state, companion1, player1):

    """
    complex

    status:
        zombie1: alive --> dead
    agent_at:
        companion1: zombie1 --> player1
    agent_looking_at:
        companion1: zombie1 --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, player1, zombie1])
    if not len(params) == 3: return False

    # type check ('player1', 'zombie1')
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False



    return [
        ('task_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead',
         companion1, player1),
        ('task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1',
         companion1)
    ]



def task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead__2(state, companion1, player1):

    """
    complex

    status:
        zombie1: alive --> dead
    agent_at:
        companion1: zombie2 --> player1
    agent_looking_at:
        companion1: zombie1 --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, player1, zombie1, zombie2])
    if not len(params) == 4: return False

    # type check ('player1', 'zombie1', 'zombie2')
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False



    return [('task_AGENT_AT_companion1_zombie1', companion1), (
        'task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead',
        companion1, player1)]



def task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie3_dead__1(state, companion1, player1, zombie1):

    """
    complex

    status:
        zombie1: alive --> dead
        zombie3: alive --> dead
    agent_at:
        companion1: zombie2 --> player1
    agent_looking_at:
        companion1: zombie3 --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, player1, zombie1, zombie2, zombie3])
    if not len(params) == 5: return False

    # type check ('player1', 'zombie1', 'zombie3', 'zombie2')
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False



    return [(
        'task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie3_dead',
        companion1, zombie1
    ), ('task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead',
        companion1, player1)]



def task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie3_dead__2(state, companion1, player1, zombie3):

    """
    complex

    status:
        zombie1: alive --> dead
        zombie3: alive --> dead
    agent_at:
        companion1: zombie2 --> player1
    agent_looking_at:
        companion1: zombie1 --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, player1, zombie1, zombie2, zombie3])
    if not len(params) == 5: return False

    # type check ('player1', 'zombie1', 'zombie3', 'zombie2')
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False



    return [(
        'task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie3_dead',
        companion1, player1, zombie3), (
            'task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1',
            companion1)]



def task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead__1(state, companion1, zombie1, zombie2):

    """
    complex

    status:
        zombie1: alive --> dead
    agent_at:
        companion1: none --> zombie1
    agent_looking_at:
        companion1: none --> zombie2
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie1, zombie2])
    if not len(params) == 4: return False

    # type check ('none', 'zombie1', 'zombie2')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie2 in state.status and 'alive' == state.status[zombie2]):
    	return False

    ('status', 'alive')
    ('agents', 'player')
    # search state to assign remaining variables

    # section 0
    player1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'player' and p in state.closest_hostile_mob
        and state.closest_hostile_mob[p] == zombie1 and p not in params
    ]
    if not (player1s): return False
    player1 = player1s[0]
    params.update([player1])

    params = set([companion1, none, player1, zombie1, zombie2])

    if not len(params) == 5:
    	raise RuntimeError('searched variables are not unique.')



    return [('task_AGENT_LOOKING_AT_companion1_zombie1', companion1, zombie1), (
        'task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead',
        companion1, zombie2)]



def task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead__2(state, companion1, zombie2):

    """
    complex

    status:
        zombie1: alive --> dead
    agent_at:
        companion1: none --> zombie1
    agent_looking_at:
        companion1: zombie1 --> zombie2
    """


    # assignment by lookup
    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie1, zombie2])
    if not len(params) == 4: return False

    # type check ('none', 'zombie1', 'zombie2')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie2 in state.status and 'alive' == state.status[zombie2]):
    	return False



    return [(
        'task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie1_dead',
        companion1), ('task_AGENT_LOOKING_AT_companion1_zombie2', companion1,
                      zombie2)]



def task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead__3(state, companion1, zombie1, zombie2):

    """
    complex

    status:
        zombie1: alive --> dead
    agent_at:
        companion1: zombie3 --> zombie1
    agent_looking_at:
        companion1: zombie3 --> zombie2
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2, zombie3])
    if not len(params) == 4: return False

    # type check ('zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie2 in state.status and 'alive' == state.status[zombie2]):
    	return False



    return [(
        'task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie1_dead',
        companion1, zombie1), ('task_AGENT_LOOKING_AT_companion1_zombie2',
                               companion1, zombie2)]



def task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie2_dead_zombie3_dead__1(state, companion1, player1, zombie1, zombie2):

    """
    complex

    status:
        zombie1: alive --> dead
        zombie3: alive --> dead
        zombie2: alive --> dead
    agent_at:
        companion1: none --> player1
    agent_looking_at:
        companion1: none --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    if (player1 in state.closest_hostile_mob and player1 in state.status
            and player1 in state.agents and 'alive' == state.status[player1]
            and 'player' == state.agents[player1]):
    	zombie3 = state.closest_hostile_mob[player1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, player1, zombie1, zombie2, zombie3])
    if not len(params) == 6: return False

    # type check ('none', 'zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False



    return [(
        'task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie2_dead_zombie3_dead',
        companion1, zombie1, zombie2, zombie3
    ), ('task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead',
        companion1, player1)]



def task_lookat_companion1_zombie2_zombie1(state, companion1, zombie2, zombie1):

    """
    primitive

    agent_looking_at: companion1: zombie2 --> zombie1
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie1' in locals()
               and companion1 in state.agent_looking_at
               and companion1 in state.status and companion1 in state.agents
               and zombie1 == state.agent_looking_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2])
    if not len(params) == 3: return False

    # type check ('companion1', 'zombie1', 'zombie2')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False

    # comparison check
    if not (zombie2 == state.agent_looking_at[companion1]): return False



    return [('LOOKAT', companion1, zombie2, zombie1),
            ('task_lookat_companion1_zombie2_zombie1', companion1, zombie2,
             zombie1)]



def task_moveto_companion1_zombie2_zombie3(state, companion1, zombie2, zombie3):

    """
    primitive

    agent_at: companion1: zombie2 --> zombie3
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie3' in locals()
               and companion1 in state.agent_at and companion1 in state.status
               and companion1 in state.agents
               and zombie3 == state.agent_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, zombie2, zombie3])
    if not len(params) == 3: return False

    # type check ('companion1', 'zombie3', 'zombie2')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False

    # comparison check
    if not (zombie3 == state.agent_looking_at[companion1]): return False
    if not (zombie2 == state.agent_at[companion1]): return False



    return [('MOVETO', companion1, zombie2, zombie3),
            ('task_moveto_companion1_zombie2_zombie3', companion1, zombie2,
             zombie3)]



def task_lookat_companion1_zombie3_zombie2(state, companion1, zombie3, zombie2):

    """
    primitive

    agent_looking_at: companion1: zombie3 --> zombie2
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'zombie2' in locals()
               and companion1 in state.agent_looking_at
               and companion1 in state.status and companion1 in state.agents
               and zombie2 == state.agent_looking_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, zombie2, zombie3])
    if not len(params) == 3: return False

    # type check ('companion1', 'zombie3', 'zombie2')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie2 in state.status and 'alive' == state.status[zombie2]):
    	return False

    # comparison check
    if not (zombie3 == state.agent_looking_at[companion1]): return False



    return [('LOOKAT', companion1, zombie3, zombie2),
            ('task_lookat_companion1_zombie3_zombie2', companion1, zombie3,
             zombie2)]



def task_lookat_companion1_zombie3_player1(state, companion1, zombie3, player1):

    """
    primitive

    agent_looking_at: companion1: zombie3 --> player1
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'player1' in locals()
               and companion1 in state.agent_looking_at
               and companion1 in state.status and companion1 in state.agents
               and player1 == state.agent_looking_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, player1, zombie3])
    if not len(params) == 3: return False

    # type check ('companion1', 'player1', 'zombie3')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False

    # comparison check
    if not (zombie3 == state.agent_looking_at[companion1]): return False



    return [('LOOKAT', companion1, zombie3, player1),
            ('task_lookat_companion1_zombie3_player1', companion1, zombie3,
             player1)]



def task_lookat_companion1_none_zombie1(state, companion1, none, zombie1):

    """
    primitive

    agent_looking_at: companion1: none --> zombie1
    """


    # initialize variables
    player1 = None

    # are effects met?
    effects = ('companion1' in locals() and 'zombie1' in locals()
               and companion1 in state.agent_looking_at
               and companion1 in state.status and companion1 in state.agents
               and zombie1 == state.agent_looking_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, none, zombie1])
    if not len(params) == 3: return False

    # type check ('companion1', 'none', 'zombie1')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False

    # comparison check
    if not (none == state.agent_looking_at[companion1]): return False



    return [('LOOKAT', companion1, none, zombie1),
            ('task_lookat_companion1_none_zombie1', companion1, none, zombie1)]



def task_moveto_companion1_zombie2_player1(state, companion1, zombie2, player1):

    """
    primitive

    agent_at: companion1: zombie2 --> player1
    """


    # initialize variables

    # are effects met?
    effects = ('companion1' in locals() and 'player1' in locals()
               and companion1 in state.agent_at and companion1 in state.status
               and companion1 in state.agents
               and player1 == state.agent_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, player1, zombie2])
    if not len(params) == 3: return False

    # type check ('companion1', 'player1', 'zombie2')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False

    # comparison check
    if not (player1 == state.agent_looking_at[companion1]): return False
    if not (zombie2 == state.agent_at[companion1]): return False



    return [('MOVETO', companion1, zombie2, player1),
            ('task_moveto_companion1_zombie2_player1', companion1, zombie2,
             player1)]



def task_lookat_companion1_none_zombie3(state, companion1, none, zombie3):

    """
    primitive

    agent_looking_at: companion1: none --> zombie3
    """


    # initialize variables
    player1 = None

    # are effects met?
    effects = ('companion1' in locals() and 'zombie3' in locals()
               and companion1 in state.agent_looking_at
               and companion1 in state.status and companion1 in state.agents
               and zombie3 == state.agent_looking_at[companion1]
               and 'companion' == state.agents[companion1]
               and 'alive' == state.status[companion1])
    if effects: return []

    # assignment by lookup

    # variable uniqueness check
    params = set([companion1, none, zombie3])
    if not len(params) == 3: return False

    # type check ('companion1', 'none', 'zombie3')
    if not (companion1 in state.status and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	return False
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False

    # comparison check
    if not (none == state.agent_looking_at[companion1]): return False



    return [('LOOKAT', companion1, none, zombie3),
            ('task_lookat_companion1_none_zombie3', companion1, none, zombie3)]



def task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie2(state, companion1, zombie2):

    """
    basic

    agent_at:
        companion1: none --> zombie2
    agent_looking_at:
        companion1: none --> zombie2
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie2])
    if not len(params) == 3: return False

    # type check ('none', 'zombie2')
    if not (zombie2 in state.status and 'alive' == state.status[zombie2]):
    	return False

    ('status', 'alive')
    ('agents', 'player')
    # search state to assign remaining variables

    # section 0
    player1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'player' and p in state.closest_hostile_mob
        and state.closest_hostile_mob[p] == zombie2 and p not in params
    ]
    if not (player1s): return False
    player1 = player1s[0]
    params.update([player1])

    params = set([companion1, none, player1, zombie2])

    if not len(params) == 4:
    	raise RuntimeError('searched variables are not unique.')



    return [('task_lookat_companion1_none_zombie2', companion1, none, zombie2),
            ('task_moveto_companion1_none_zombie2', companion1, none, zombie2)]



def task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie1_dead(state, companion1, zombie3):

    """
    basic

    status:
        zombie1: alive --> dead
    agent_at:
        companion1: zombie2 --> zombie1
    agent_looking_at:
        companion1: zombie1 --> zombie3
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2, zombie3])
    if not len(params) == 4: return False

    # type check ('zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False



    return [('task_moveto_companion1_zombie2_zombie1', companion1, zombie2,
             zombie1), ('task_attack_companion1_zombie1', companion1, zombie1),
            ('task_lookat_companion1_zombie1_zombie3', companion1, zombie1,
             zombie3)]



def task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie3(state, companion1, zombie3):

    """
    basic

    agent_at:
        companion1: none --> zombie3
    agent_looking_at:
        companion1: none --> zombie3
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie3])
    if not len(params) == 3: return False

    # type check ('none', 'zombie3')
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False

    ('status', 'alive')
    ('agents', 'player')
    # search state to assign remaining variables

    # section 0
    player1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'player' and p in state.closest_hostile_mob
        and state.closest_hostile_mob[p] == zombie3 and p not in params
    ]
    if not (player1s): return False
    player1 = player1s[0]
    params.update([player1])

    params = set([companion1, none, player1, zombie3])

    if not len(params) == 4:
    	raise RuntimeError('searched variables are not unique.')



    return [('task_lookat_companion1_none_zombie3', companion1, none, zombie3),
            ('task_moveto_companion1_none_zombie3', companion1, none, zombie3)]



def task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie3_dead(state, companion1, player1):

    """
    complex

    status:
        zombie3: alive --> dead
    agent_at:
        companion1: zombie2 --> player1
    agent_looking_at:
        companion1: zombie3 --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, player1, zombie2, zombie3])
    if not len(params) == 4: return False

    # type check ('player1', 'zombie3', 'zombie2')
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False



    return [(
        'task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie3_dead',
        companion1, player1), (
            'task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1',
            companion1)]



def task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie1_dead_zombie2_dead(state, companion1, zombie1, zombie2, zombie3):

    """
    complex

    status:
        zombie1: alive --> dead
        zombie2: alive --> dead
    agent_at:
        companion1: none --> zombie2
    agent_looking_at:
        companion1: none --> zombie3
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie1, zombie2, zombie3])
    if not len(params) == 5: return False

    # type check ('none', 'zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False

    ('status', 'alive')
    ('agents', 'player')
    # search state to assign remaining variables

    # section 0
    player1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'player' and p in state.closest_hostile_mob
        and state.closest_hostile_mob[p] == zombie1 and p not in params
    ]
    if not (player1s): return False
    player1 = player1s[0]
    params.update([player1])

    params = set([none, companion1, player1, zombie1, zombie3, zombie2])

    if not len(params) == 6:
    	raise RuntimeError('searched variables are not unique.')



    return [(
        'task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead',
        companion1, zombie1, zombie2
    ), ('task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie2_dead',
        companion1, zombie3)]



def task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie3_dead(state, companion1, player1, zombie3):

    """
    complex

    status:
        zombie1: alive --> dead
        zombie3: alive --> dead
    agent_at:
        companion1: zombie2 --> zombie3
    agent_looking_at:
        companion1: zombie1 --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, player1, zombie1, zombie2, zombie3])
    if not len(params) == 5: return False

    # type check ('player1', 'zombie1', 'zombie3', 'zombie2')
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False



    return [(
        'task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie1_dead',
        companion1, zombie3
    ), ('task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie3_dead',
        companion1, player1)]



def task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie3_dead(state, companion1, zombie3):

    """
    complex

    status:
        zombie3: alive --> dead
    agent_at:
        companion1: none --> zombie3
    agent_looking_at:
        companion1: none --> zombie3
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie3])
    if not len(params) == 3: return False

    # type check ('none', 'zombie3')
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False

    # search state to assign remaining variables

    # section 0
    player1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'player' and p in state.closest_hostile_mob
        and state.closest_hostile_mob[p] == zombie3 and p not in params
    ]
    if not (player1s): return False
    player1 = player1s[0]
    params.update([player1])

    params = set([companion1, none, player1, zombie3])

    if not len(params) == 4:
    	raise RuntimeError('searched variables are not unique.')



    return [
        ('task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie3',
         companion1, zombie3), ('task_STATUS_zombie3_dead', zombie3)
    ]



def task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie1_dead(state, companion1, zombie3):

    """
    complex

    status:
        zombie1: alive --> dead
    agent_at:
        companion1: zombie2 --> zombie3
    agent_looking_at:
        companion1: zombie1 --> zombie3
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2, zombie3])
    if not len(params) == 4: return False

    # type check ('zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False



    return [(
        'task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie1_dead',
        companion1, zombie3), ('task_AGENT_AT_companion1_zombie3', companion1)]



def task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead_zombie3_dead(state, companion1, zombie1, zombie2, zombie3):

    """
    complex

    status:
        zombie1: alive --> dead
        zombie3: alive --> dead
    agent_at:
        companion1: none --> zombie1
    agent_looking_at:
        companion1: none --> zombie2
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie1, zombie2, zombie3])
    if not len(params) == 5: return False

    # type check ('none', 'zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False
    if not (zombie2 in state.status and 'alive' == state.status[zombie2]):
    	return False

    ('status', 'alive')
    ('agents', 'player')
    # search state to assign remaining variables

    # section 0
    player1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'player' and p in state.closest_hostile_mob
        and state.closest_hostile_mob[p] == zombie3 and p not in params
    ]
    if not (player1s): return False
    player1 = player1s[0]
    params.update([player1])

    params = set([none, companion1, player1, zombie1, zombie3, zombie2])

    if not len(params) == 6:
    	raise RuntimeError('searched variables are not unique.')



    return [(
        'task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie3_dead',
        companion1, zombie3
    ), ('task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead',
        companion1, zombie1, zombie2)]



def task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie2_dead(state, companion1, zombie2):

    """
    complex

    status:
        zombie2: alive --> dead
    agent_at:
        companion1: none --> zombie2
    agent_looking_at:
        companion1: none --> zombie2
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie2])
    if not len(params) == 3: return False

    # type check ('none', 'zombie2')
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False

    ('status', 'alive')
    ('agents', 'player')
    # search state to assign remaining variables

    # section 0
    player1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'player' and p in state.closest_hostile_mob
        and state.closest_hostile_mob[p] == zombie2 and p not in params
    ]
    if not (player1s): return False
    player1 = player1s[0]
    params.update([player1])

    params = set([companion1, none, player1, zombie2])

    if not len(params) == 4:
    	raise RuntimeError('searched variables are not unique.')



    return [
        ('task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie2',
         companion1, zombie2),
        ('task_AGENT_AT_companion1_zombie2_STATUS_zombie2_dead', zombie2)
    ]



def task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie2_dead_zombie3_dead(state, companion1, zombie1, zombie2, zombie3):

    """
    complex

    status:
        zombie3: alive --> dead
        zombie2: alive --> dead
    agent_at:
        companion1: none --> zombie2
    agent_looking_at:
        companion1: none --> zombie1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie1, zombie2, zombie3])
    if not len(params) == 5: return False

    # type check ('none', 'zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False

    ('status', 'alive')
    ('agents', 'player')
    # search state to assign remaining variables

    # section 0
    player1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'player' and p in state.closest_hostile_mob
        and state.closest_hostile_mob[p] == zombie3 and p not in params
    ]
    if not (player1s): return False
    player1 = player1s[0]
    params.update([player1])

    params = set([none, companion1, player1, zombie1, zombie3, zombie2])

    if not len(params) == 6:
    	raise RuntimeError('searched variables are not unique.')



    return [(
        'task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie3_dead',
        companion1, zombie2, zombie3
    ), ('task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie2_dead',
        companion1, zombie1)]



def task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie3_dead__1(state, companion1, zombie1):

    """
    complex

    status:
        zombie3: alive --> dead
    agent_looking_at:
        companion1: zombie3 --> zombie1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie3])
    if not len(params) == 3: return False

    # type check ('zombie1', 'zombie3')
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False



    return [('task_STATUS_zombie3_dead', zombie3),
            ('task_AGENT_LOOKING_AT_companion1_zombie1', companion1, zombie1)]



def task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie3_dead__2(state, companion1, zombie1):

    """
    complex

    status:
        zombie3: alive --> dead
    agent_at:
        companion1: zombie2 --> zombie3
    agent_looking_at:
        companion1: zombie3 --> zombie1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_looking_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2, zombie3])
    if not len(params) == 4: return False

    # type check ('zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False



    return [('task_AGENT_AT_companion1_zombie3', companion1), (
        'task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie3_dead',
        companion1, zombie1)]



def task_AGENT_LOOKING_AT_companion1_zombie3(state, companion1, zombie3):

    """
    basic

    agent_looking_at: companion1: zombie2 --> zombie3
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie2, zombie3])
    if not len(params) == 3: return False

    # type check ('zombie3', 'zombie2')
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False



    return [('task_lookat_companion1_zombie2_zombie3', companion1, zombie2,
             zombie3)]



def task_STATUS_zombie3_dead(state, zombie3):

    """
    basic

    status: zombie3: alive --> dead
    """


    # assignment by lookup

    # variable uniqueness check
    params = set([zombie3])
    if not len(params) == 1: return False

    # type check ('zombie3',)
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False

    ('status', 'alive')
    ('agents', 'companion')
    # search state to assign remaining variables

    # section 0
    companion1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'companion' and p in state.agent_looking_at
        and state.agent_looking_at[p] == zombie3 and p not in params
    ]
    if not (companion1s): return False
    companion1 = companion1s[0]
    params.update([companion1])

    params = set([companion1, zombie3])

    if not len(params) == 2:
    	raise RuntimeError('searched variables are not unique.')



    return [('task_attack_companion1_zombie3', companion1, zombie3)]



def task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie2_dead__1(state, companion1, zombie3):

    """
    basic

    status:
        zombie2: alive --> dead
    agent_at:
        companion1: zombie1 --> zombie2
    agent_looking_at:
        companion1: zombie2 --> zombie3
    """


    # assignment by lookup
    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2, zombie3])
    if not len(params) == 4: return False

    # type check ('zombie1', 'zombie3', 'zombie2')
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False



    return [('task_moveto_companion1_zombie1_zombie2', companion1, zombie1,
             zombie2), ('task_attack_companion1_zombie2', companion1, zombie2),
            ('task_lookat_companion1_zombie2_zombie3', companion1, zombie2,
             zombie3)]



def task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie2_dead__2(state, companion1, zombie2, zombie3):

    """
    complex

    status:
        zombie2: alive --> dead
    agent_at:
        companion1: none --> zombie2
    agent_looking_at:
        companion1: none --> zombie3
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie2, zombie3])
    if not len(params) == 4: return False

    # type check ('none', 'zombie3', 'zombie2')
    if not (zombie3 in state.status and 'alive' == state.status[zombie3]):
    	return False
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False

    ('status', 'alive')
    ('agents', 'player')
    # search state to assign remaining variables

    # section 0
    player1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'player' and p in state.closest_hostile_mob
        and state.closest_hostile_mob[p] == zombie2 and p not in params
    ]
    if not (player1s): return False
    player1 = player1s[0]
    params.update([player1])

    params = set([companion1, none, player1, zombie3, zombie2])

    if not len(params) == 5:
    	raise RuntimeError('searched variables are not unique.')



    return [(
        'task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie2_dead',
        companion1, zombie2), ('task_AGENT_LOOKING_AT_companion1_zombie3',
                               companion1, zombie3)]



def task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie2_dead__1(state, companion1, zombie1):

    """
    basic

    status:
        zombie2: alive --> dead
    agent_at:
        companion1: zombie3 --> zombie2
    agent_looking_at:
        companion1: zombie2 --> zombie1
    """


    # assignment by lookup
    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2, zombie3])
    if not len(params) == 4: return False

    # type check ('zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False



    return [('task_moveto_companion1_zombie3_zombie2', companion1, zombie3,
             zombie2), ('task_attack_companion1_zombie2', companion1, zombie2),
            ('task_lookat_companion1_zombie2_zombie1', companion1, zombie2,
             zombie1)]



def task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie2_dead__2(state, companion1, zombie1, zombie2):

    """
    complex

    status:
        zombie2: alive --> dead
    agent_at:
        companion1: none --> zombie2
    agent_looking_at:
        companion1: none --> zombie1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, zombie1, zombie2])
    if not len(params) == 4: return False

    # type check ('none', 'zombie1', 'zombie2')
    if not (zombie1 in state.status and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False

    ('status', 'alive')
    ('agents', 'player')
    # search state to assign remaining variables

    # section 0
    player1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'player' and p in state.closest_hostile_mob
        and state.closest_hostile_mob[p] == zombie2 and p not in params
    ]
    if not (player1s): return False
    player1 = player1s[0]
    params.update([player1])

    params = set([companion1, none, player1, zombie1, zombie2])

    if not len(params) == 5:
    	raise RuntimeError('searched variables are not unique.')



    return [(
        'task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie2_dead',
        companion1, zombie2), ('task_AGENT_LOOKING_AT_companion1_zombie1',
                               companion1, zombie1)]



def task_AGENT_LOOKING_AT_companion1_player1__1(state, companion1, player1):

    """
    basic

    agent_looking_at: companion1: zombie3 --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie3 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, player1, zombie3])
    if not len(params) == 3: return False

    # type check ('player1', 'zombie3')
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False



    return [('task_lookat_companion1_zombie3_player1', companion1, zombie3,
             player1)]



def task_AGENT_LOOKING_AT_companion1_player1__2(state, companion1, player1):

    """
    basic

    agent_looking_at: companion1: zombie1 --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, player1, zombie1])
    if not len(params) == 3: return False

    # type check ('player1', 'zombie1')
    if not (player1 in state.status and 'alive' == state.status[player1]):
    	return False



    return [('task_lookat_companion1_zombie1_player1', companion1, zombie1,
             player1)]



def task_AGENT_AT_companion1_zombie2_STATUS_zombie2_dead__1(state, zombie2):

    """
    basic

    status: zombie2: alive --> dead
    """


    # assignment by lookup

    # variable uniqueness check
    params = set([zombie2])
    if not len(params) == 1: return False

    # type check ('zombie2',)
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False

    ('status', 'alive')
    ('agents', 'companion')
    # search state to assign remaining variables

    # section 0
    companion1s = [
        p for p in (set(state.agents) & set(state.status))
        if p in state.status and state.status[p] == 'alive' and p in state.agents
        and state.agents[p] == 'companion' and p in state.agent_looking_at
        and state.agent_looking_at[p] == zombie2 and p not in params
    ]
    if not (companion1s): return False
    companion1 = companion1s[0]
    params.update([companion1])

    params = set([companion1, zombie2])

    if not len(params) == 2:
    	raise RuntimeError('searched variables are not unique.')



    return [('task_attack_companion1_zombie2', companion1, zombie2)]



def task_AGENT_AT_companion1_zombie2_STATUS_zombie2_dead__2(state, companion1):

    """
    basic

    status:
        zombie2: alive --> dead
    agent_at:
        companion1: zombie1 --> zombie2
    """


    # assignment by lookup
    if (companion1 in state.agent_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie1 = state.agent_at[companion1]
    else:
    	return False

    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	zombie2 = state.agent_looking_at[companion1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, zombie1, zombie2])
    if not len(params) == 3: return False

    # type check ('zombie1', 'zombie2')
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False



    return [('task_moveto_companion1_zombie1_zombie2', companion1, zombie1,
             zombie2), ('task_attack_companion1_zombie2', companion1, zombie2)]



def task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie2_dead_zombie3_dead__2(state, companion1, player1, zombie1, zombie3):

    """
    complex

    status:
        zombie1: alive --> dead
        zombie3: alive --> dead
        zombie2: alive --> dead
    agent_at:
        companion1: none --> player1
    agent_looking_at:
        companion1: none --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    if (player1 in state.closest_hostile_mob and player1 in state.status
            and player1 in state.agents and 'alive' == state.status[player1]
            and 'player' == state.agents[player1]):
    	zombie2 = state.closest_hostile_mob[player1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, player1, zombie1, zombie2, zombie3])
    if not len(params) == 6: return False

    # type check ('none', 'zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False



    return [(
        'task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie2_dead',
        companion1, zombie1, zombie2
    ), ('task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie3_dead',
        companion1, player1, zombie3)]



def task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie2_dead_zombie3_dead__3(state, companion1, player1, zombie1, zombie3):

    """
    complex

    status:
        zombie1: alive --> dead
        zombie3: alive --> dead
        zombie2: alive --> dead
    agent_at:
        companion1: none --> player1
    agent_looking_at:
        companion1: none --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    if (player1 in state.closest_hostile_mob and player1 in state.status
            and player1 in state.agents and 'alive' == state.status[player1]
            and 'player' == state.agents[player1]):
    	zombie2 = state.closest_hostile_mob[player1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, player1, zombie1, zombie2, zombie3])
    if not len(params) == 6: return False

    # type check ('none', 'zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False



    return [(
        'task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie2_dead',
        companion1, zombie2, zombie3
    ), ('task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie3_dead',
        companion1, player1, zombie1)]



def task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie2_dead_zombie3_dead__4(state, companion1, player1, zombie2, zombie3):

    """
    complex

    status:
        zombie1: alive --> dead
        zombie3: alive --> dead
        zombie2: alive --> dead
    agent_at:
        companion1: none --> player1
    agent_looking_at:
        companion1: none --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    if (player1 in state.closest_hostile_mob and player1 in state.status
            and player1 in state.agents and 'alive' == state.status[player1]
            and 'player' == state.agents[player1]):
    	zombie1 = state.closest_hostile_mob[player1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, player1, zombie1, zombie2, zombie3])
    if not len(params) == 6: return False

    # type check ('none', 'zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False



    return [(
        'task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie1_dead_zombie2_dead',
        companion1, zombie1, zombie2, zombie3
    ), ('task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie3_dead',
        companion1, player1)]



def task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie2_dead_zombie3_dead__5(state, companion1, player1, zombie1, zombie2):

    """
    complex

    status:
        zombie1: alive --> dead
        zombie3: alive --> dead
        zombie2: alive --> dead
    agent_at:
        companion1: none --> player1
    agent_looking_at:
        companion1: none --> player1
    """


    # assignment by lookup
    if (companion1 in state.agent_looking_at and companion1 in state.status
            and companion1 in state.agents
            and 'companion' == state.agents[companion1]
            and 'alive' == state.status[companion1]):
    	none = state.agent_looking_at[companion1]
    else:
    	return False

    if (player1 in state.closest_hostile_mob and player1 in state.status
            and player1 in state.agents and 'alive' == state.status[player1]
            and 'player' == state.agents[player1]):
    	zombie3 = state.closest_hostile_mob[player1]
    else:
    	return False

    # variable uniqueness check
    params = set([companion1, none, player1, zombie1, zombie2, zombie3])
    if not len(params) == 6: return False

    # type check ('none', 'zombie1', 'zombie3', 'zombie2')
    if not (zombie1 in state.status and zombie1 in state.mobs and
            'zombie' == state.mobs[zombie1] and 'alive' == state.status[zombie1]):
    	return False
    if not (zombie3 in state.status and zombie3 in state.mobs and
            'zombie' == state.mobs[zombie3] and 'alive' == state.status[zombie3]):
    	return False
    if not (zombie2 in state.status and zombie2 in state.mobs and
            'alive' == state.status[zombie2] and 'zombie' == state.mobs[zombie2]):
    	return False



    return [(
        'task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead_zombie2_dead_zombie3_dead',
        companion1, zombie1, zombie2, zombie3), (
            'task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1',
            companion1, player1)]



planner.declare_methods('task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead', *[
task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead__1,
task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead__2
])

planner.declare_methods('task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1', *[
task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1__1,
task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1__2,
task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1__3
])

planner.declare_methods('task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead_zombie3_dead', task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead_zombie3_dead)

planner.declare_methods('task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie2_dead_zombie3_dead', task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie2_dead_zombie3_dead)

planner.declare_methods('task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie1_dead_zombie2_dead', task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie1_dead_zombie2_dead)

planner.declare_methods('task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie3_dead', *[
task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie3_dead__1,
task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie3_dead__2
])

planner.declare_methods('task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie1_dead', task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie1_dead)

planner.declare_methods('task_AGENT_LOOKING_AT_companion1_player1', *[
task_AGENT_LOOKING_AT_companion1_player1__1,
task_AGENT_LOOKING_AT_companion1_player1__2
])

planner.declare_methods('task_AGENT_LOOKING_AT_companion1_zombie3', task_AGENT_LOOKING_AT_companion1_zombie3)

planner.declare_methods('task_attack_companion1_zombie3', task_attack_companion1_zombie3)

planner.declare_methods('task_lookat_companion1_zombie1_player1', task_lookat_companion1_zombie1_player1)

planner.declare_methods('task_lookat_companion1_zombie2_zombie1', task_lookat_companion1_zombie2_zombie1)

planner.declare_methods('task_lookat_companion1_zombie3_zombie2', task_lookat_companion1_zombie3_zombie2)

planner.declare_methods('task_moveto_companion1_zombie1_player1', task_moveto_companion1_zombie1_player1)

planner.declare_methods('task_moveto_companion1_zombie2_zombie1', task_moveto_companion1_zombie2_zombie1)

planner.declare_methods('task_moveto_companion1_zombie3_zombie2', task_moveto_companion1_zombie3_zombie2)

planner.declare_methods('task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie2_dead_zombie3_dead', *[
task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie2_dead_zombie3_dead__1,
task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie2_dead_zombie3_dead__2,
task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie2_dead_zombie3_dead__3,
task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie2_dead_zombie3_dead__4,
task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie2_dead_zombie3_dead__5
])

planner.declare_methods('task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie1_dead', *[
task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie1_dead__1,
task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie1_dead__2,
task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie1_dead__3
])

planner.declare_methods('task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie1_dead', task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie1_dead)

planner.declare_methods('task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie2', task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie2)

planner.declare_methods('task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie2_dead', *[
task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie2_dead__1,
task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie2_dead__2
])

planner.declare_methods('task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie3_dead', *[
task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie3_dead__1,
task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie3_dead__2
])

planner.declare_methods('task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie3_dead', task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie3_STATUS_zombie3_dead)

planner.declare_methods('task_AGENT_LOOKING_AT_companion1_zombie1', *[
task_AGENT_LOOKING_AT_companion1_zombie1__1,
task_AGENT_LOOKING_AT_companion1_zombie1__2,
task_AGENT_LOOKING_AT_companion1_zombie1__3
])

planner.declare_methods('task_attack_companion1_zombie1', task_attack_companion1_zombie1)

planner.declare_methods('task_lookat_companion1_none_zombie2', task_lookat_companion1_none_zombie2)

planner.declare_methods('task_lookat_companion1_zombie1_zombie3', task_lookat_companion1_zombie1_zombie3)

planner.declare_methods('task_lookat_companion1_zombie3_player1', task_lookat_companion1_zombie3_player1)

planner.declare_methods('task_moveto_companion1_none_zombie2', task_moveto_companion1_none_zombie2)

planner.declare_methods('task_moveto_companion1_zombie1_zombie3', task_moveto_companion1_zombie1_zombie3)

planner.declare_methods('task_moveto_companion1_zombie3_player1', task_moveto_companion1_zombie3_player1)

planner.declare_methods('task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie3_dead', *[
task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie3_dead__1,
task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie3_dead__2
])

planner.declare_methods('task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie3_dead', task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie3_dead)

planner.declare_methods('task_AGENT_AT_companion1_zombie1', *[
task_AGENT_AT_companion1_zombie1__1,
task_AGENT_AT_companion1_zombie1__2,
task_AGENT_AT_companion1_zombie1__3
])

planner.declare_methods('task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead_zombie2_dead_zombie3_dead', task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead_zombie2_dead_zombie3_dead)

planner.declare_methods('task_AGENT_AT_companion1_zombie2_STATUS_zombie2_dead', *[
task_AGENT_AT_companion1_zombie2_STATUS_zombie2_dead__1,
task_AGENT_AT_companion1_zombie2_STATUS_zombie2_dead__2
])

planner.declare_methods('task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie3_dead', task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie3_dead)

planner.declare_methods('task_AGENT_AT_companion1_zombie3', *[
task_AGENT_AT_companion1_zombie3__1,
task_AGENT_AT_companion1_zombie3__2
])

planner.declare_methods('task_AGENT_LOOKING_AT_companion1_zombie2', *[
task_AGENT_LOOKING_AT_companion1_zombie2__1,
task_AGENT_LOOKING_AT_companion1_zombie2__2
])

planner.declare_methods('task_attack_companion1_zombie2', task_attack_companion1_zombie2)

planner.declare_methods('task_lookat_companion1_none_zombie3', task_lookat_companion1_none_zombie3)

planner.declare_methods('task_lookat_companion1_zombie2_player1', task_lookat_companion1_zombie2_player1)

planner.declare_methods('task_lookat_companion1_zombie3_zombie1', task_lookat_companion1_zombie3_zombie1)

planner.declare_methods('task_moveto_companion1_none_zombie3', task_moveto_companion1_none_zombie3)

planner.declare_methods('task_moveto_companion1_zombie2_player1', task_moveto_companion1_zombie2_player1)

planner.declare_methods('task_moveto_companion1_zombie3_zombie1', task_moveto_companion1_zombie3_zombie1)

planner.declare_methods('task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie3_dead', task_AGENT_AT_companion1_player1_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie3_dead)

planner.declare_methods('task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead', *[
task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead__1,
task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead__2,
task_AGENT_AT_companion1_zombie1_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie1_dead__3
])

planner.declare_methods('task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie2_dead', *[
task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie2_dead__1,
task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie1_STATUS_zombie2_dead__2
])

planner.declare_methods('task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie2_dead', task_AGENT_AT_companion1_zombie2_AGENT_LOOKING_AT_companion1_zombie2_STATUS_zombie2_dead)

planner.declare_methods('task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie3_dead', task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead_zombie3_dead)

planner.declare_methods('task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie3', task_AGENT_AT_companion1_zombie3_AGENT_LOOKING_AT_companion1_zombie3)

planner.declare_methods('task_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead', task_AGENT_LOOKING_AT_companion1_player1_STATUS_zombie1_dead)

planner.declare_methods('task_STATUS_zombie3_dead', task_STATUS_zombie3_dead)

planner.declare_methods('task_lookat_companion1_none_zombie1', task_lookat_companion1_none_zombie1)

planner.declare_methods('task_lookat_companion1_zombie1_zombie2', task_lookat_companion1_zombie1_zombie2)

planner.declare_methods('task_lookat_companion1_zombie2_zombie3', task_lookat_companion1_zombie2_zombie3)

planner.declare_methods('task_moveto_companion1_none_zombie1', task_moveto_companion1_none_zombie1)

planner.declare_methods('task_moveto_companion1_zombie1_zombie2', task_moveto_companion1_zombie1_zombie2)

planner.declare_methods('task_moveto_companion1_zombie2_zombie3', task_moveto_companion1_zombie2_zombie3)
