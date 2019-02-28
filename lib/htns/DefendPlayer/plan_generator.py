from collections import defaultdict
from os.path import join as joinpath
from os.path import dirname, splitext, basename
import sys
from copy import deepcopy
from importlib import import_module
from itertools import product, chain, repeat
import networkx as nx


# domain should import whatever version of planner as planner
from minecraft_pyhop import *
import htn

atom_delim = "-"

def dict_to_state(dict_state, state=None, state_name=""):
    """
    returns a planner State object based on dict_state and state.
    Changes neither.
    """
    dict_state = deepcopy(dict_state)  # protect original dict_state
    if not state:
        state = planner.State(state_name)
    else:
        state = deepcopy(state)
    for name, section in dict_state.items():
        if hasattr(state, name):
            getattr(state, name).update(**section)
        else:
            setattr(state, name, section)
    return state


def dictify_atomized_state(atom_set):
    """
    convert a list of atoms to a dict representation
    throws a TypeError if atom_set is a dict
    throws a Value Error if atoms have more than 3 parts (separated by atom_delim) or less than 2
    """
    if isinstance(atom_set, dict):
        raise TypeError("dictify_atomized_state accepts a list or set of strings")
    state = defaultdict(dict)
    for token in atom_set:
        parts = [i.strip() for i in token.split(atom_delim)]

        if len(parts) == 2:
            state[parts[0]][parts[1]] = ""
        elif len(parts) == 3:
            state[parts[0]][parts[1]] = parts[2]
        else:
            msg = "atom {} must have 2 or 3 elements separated by '-'.".format(token)
            raise ValueError(msg)
    return dict(state)


def get_action_string(node):
    """
    return a string representing the action contained in node
    given a planner node, get the action and if action has arguments,
    append arguments for that action as a string to the end of the action string
    """
    a = node["action"]
    node["cond"] = tuple([str(c) for c in node["cond"]])
    action = a + str(node["cond"]) if (a != "Finished" and a != "branch") else a
    return action

def plantree_to_graph(plan):
    """
    convert the plan output by planner into a networkx graph
    """
    graph = nx.DiGraph()
    graph.root = plan.num
    queue = [(plan,)] # plan is the first node
    all_nodes = {}

    # iterate through plan,
    # adding each unique instance of action and node data to graph
    while queue:

        element = queue.pop(0)
        node = element[0]

        if not node:# or node.num in graph:
            continue

        if node.num in graph:
            if len(element) > 1:
                graph.add_edge(element[1], node.num)
            continue

        node_data = vars(node)
        try:
            del node_data['Fexp']
            del node_data['Bexp']
            del node_data['dBexp']
            del node_data['oChanges']
            del node_data['oBexp']
            del node_data['Rexp']
            del node_data['found']
            del node_data['prev']
        except Exception as e:
            pass

        # add child
        graph.add_node(node.num, **node_data)
        action = get_action_string(node_data)

        assert action + str(node.state) not in all_nodes
        all_nodes[action + str(node.state)] = node_data
        # add edge between parent and child
        if len(element) > 1:
                graph.add_edge(element[1], node.num)

        # add the next node and the branching nodes to the queue
        branch_values = list(node.branch.values())
        children = [(i, node.num) for i in [node.next]+branch_values if i]
        queue.extend(children)

    return graph

def plan_sequence(plan, operators=ops):

    g = plantree_to_graph(plan)
    op_names = [o.__name__ for o in operators]
    longest_path = max([i for i in nx.all_simple_paths(g, plan.num, -1)])
    for i in longest_path:
        action = g.node[i]['action']
        if action == 'branch':
            continue
        elif action in op_names:
            yield action, g.node[i]['cond']


def guess_type_from_name(variable_names, types):
    for v in variable_names:
        for tp in types:
            if tp in v:
                yield v,tp
                break

def yield_f_state_args(state, task_by_num_mobs, types):
    """
    given a planner state object, a dict of tasks keyed by # of zombies,
    and a list of type strings, yield tasks and their args that are appropriate
    given the state.
    """
    s = {k:v for k,v in vars(state).items() if not k == "__name__"}
    by_type = {t: [] for t in types}
    for k, subdict in s.items():
        for k1, v1 in subdict.items():
            if v1 in types:
                by_type[v1].append(k1)

    zombies = [z for z in state.mobs if state.mobs[z] == "zombie"
               and state.status[z] == "alive"]
    c = len(zombies)

    potentially_relevant = list(chain(*[zip(repeat(t), planner.methods[t])
                                        for t in task_by_num_mobs[c]]))
    for t, f in potentially_relevant:
        code = f.__code__
        fvars = (code.co_varnames[:code.co_argcount])[1:] # skip state variable
        #print fvars
        type_guesses = dict(list(guess_type_from_name(fvars, types)))
        #print fvars, type_guesses
        argsets = [p for p in product(*[by_type[type_guesses[v]] for v in fvars])]
        for args in argsets:
            if f(state, *args):
                yield t, args


# sort the tasks into groups by the number of zombies mentioned in the title
task_by_num_mobs = defaultdict(list)
for task in planner.methods.keys():
    if task.lower() == task:
        continue
    terms = task.split("_")
    terms = [z for z in terms if "zombie" in z]
    terms = set(terms)
    task_by_num_mobs[len(terms)].append(task)

for k in task_by_num_mobs:
    task_by_num_mobs[k] = sorted(task_by_num_mobs[k], key=len, reverse=True)


def generate_plan(state_atoms, state_name="", verbose=0):
    global task_by_num_mobs, types
    state_atoms = [a.lower() for a in state_atoms]
    state_dict = dictify_atomized_state(state_atoms)
    state = dict_to_state(state_dict)
    state.__name__ = state_name
    potentials = yield_f_state_args(state, task_by_num_mobs, types)
    potentials = list(potentials)
    #print len(potentials)
    #print potentials

    for task_name, task_args in potentials:
        if verbose > 0:
            print("\n")
        task = (task_name,) + tuple(task_args)
        if verbose > 0:
            print(task)
        try:
            policy = planner.run(deepcopy(state), [task], verbose=verbose, k=0, kMax=0)
        except Exception as e:
            if verbose > 0:
                print("Planning failed. Exception:", e)
            continue

        if not policy:
            continue

        # if planner returned a sequence of actions, no further processing needed
        if isinstance(policy, list) and policy:
            return policy

        # if planner is treehop, extract the shortest sequence of actions
        plan = list((i[0],) + i[1] for i in plan_sequence(policy))
        if not plan:
            continue
        return plan
    return []



def process_trace_file_content(trace_file_content):
    """
    split the start and end states from the traces, then splits the traces and tokenizes them.
    :param trace_file_content:
    :return: all tokenized traces, initial state (as a list of atoms), final state (as a list of atoms)
    """

    traces = trace_file_content
    initial_state, final_state = [], []
    try:
        initial_state, traces = traces.split("START")
        initial_state = initial_state.strip().split("\n")
    except:
        pass

    try:
        traces, final_state = traces.split("END")
        final_state = final_state.strip().split("\n")
    except:
        pass

    traces = traces.strip().split("\n\n")
    traces = [t.split("\n") for t in traces]
    return traces, initial_state, final_state




if __name__ == "__main__":
    from pprint import pprint
    import os
    import glob
    pprint (dict(task_by_num_mobs))

    # read in the traces
    f = "/Users/morganfine-morris/Documents/Graduate School/Research/PYHOP/minecraft/kill3zombies_det"
    f = joinpath(f, "traces")
    print(f)
    if os.path.exists(f):
        trace_files = glob.glob(joinpath(f,"*"))
        initial_states = []
        for fname in trace_files:
            with open(fname, "r") as h:
                data = h.read()
            ts, i, f = process_trace_file_content(data)
            initial_states.append(i)
        for state_atoms in initial_states:
            print(generate_plan(state_atoms, "test", 0))


    state_atoms = [
         'agent_at-companion1-none',
         'agent_at-player1-none',
         'agent_looking_at-companion1-none',
         'agent_looking_at-player1-none',
         'agents-companion1-companion',
         'agents-player1-player',
         'closest_hostile_mob-player1-zombie2',
         'mobs-zombie1-zombie',
         'mobs-zombie2-zombie',
         'mobs-zombie3-zombie',
         'status-companion1-alive',
         'status-player1-alive',
         'status-zombie1-alive',
         'status-zombie2-alive',
         'status-zombie3-alive'
         ]

    print(generate_plan(state_atoms, "test", 0))
