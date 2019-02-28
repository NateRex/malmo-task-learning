"""
Pyhop, version 1.2.2 -- a simple SHOP-like planner written in Python.
Author: Dana S. Nau, 2013.05.31

Copyright 2013 Dana S. Nau - http://www.cs.umd.edu/~nau

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Pyhop should work correctly in both Python 2.7 and Python 3.2.
For examples of how to use it, see the example files that come with Pyhop.

Pyhop provides the following classes and functions:

- foo = State('foo') tells Pyhop to create an empty state object named 'foo'.
  To put variables and values into it, you should do assignments such as
  foo.var1 = val1

- bar = Goal('bar') tells Pyhop to create an empty goal object named 'bar'.
  To put variables and values into it, you should do assignments such as
  bar.var1 = val1

- print_state(foo) will print the variables and values in the state foo.

- print_goal(foo) will print the variables and values in the goal foo.

- declare_operators(o1, o2, ..., ok) tells Pyhop that o1, o2, ..., ok
  are all of the planning operators; this supersedes any previous call
  to declare_operators.

- print_operators() will print out the list of available operators.

- declare_methods('foo', m1, m2, ..., mk) tells Pyhop that m1, m2, ..., mk
  are all of the methods for tasks having 'foo' as their taskname; this
  supersedes any previous call to declare_methods('foo', ...).

- print_methods() will print out a list of all declared methods.

- pyhop(state1,tasklist) tells Pyhop to find a plan for accomplishing tasklist
  (a list of tasks), starting from an initial state state1, using whatever
  methods and operators you declared previously.

- In the above call to pyhop, you can add an optional 3rd argument called
  'verbose' that tells pyhop how much debugging printout it should provide:
- if verbose = 0 (the default), pyhop returns the solution but prints nothing;
- if verbose = 1, it prints the initial parameters and the answer;
- if verbose = 2, it also prints a message on each recursive call;
- if verbose = 3, it also prints info about what it is computing.
"""

# The Pyhop planning algorithm is very similar to the one in SHOP and JSHOP
# (see http://www.cs.umd.edu/projects/shop). Like SHOP and JSHOP, Pyhop uses
# HTN methods to decompose tasks into smaller and smaller subtasks, until it
# finds tasks that correspond directly to actions. But Pyhop differs from
# SHOP and JSHOP in several ways that should make it easier to use Pyhop
# as part of other programs:
#
# (1) In Pyhop, one writes methods and operators as ordinary Python functions
#     (rather than using a special-purpose language, as in SHOP and JSHOP).
#
# (2) Instead of representing states as collections of logical assertions,
#     Pyhop uses state-variable representation: a state is a Python object
#     that contains variable bindings. For example, to define a state in
#     which box b is located in room r1, you might write something like this:
#     s = State()
#     s.loc['b'] = 'r1'
#
# (3) You also can define goals as Python objects. For example, to specify
#     that a goal of having box b in room r2, you might write this:
#     g = Goal()
#     g.loc['b'] = 'r2'
#     Like most HTN planners, Pyhop will ignore g unless you explicitly
#     tell it what to do with g. You can do that by referring to g in
#     your methods and operators, and passing g to them as an argument.
#     In the same fashion, you could tell Pyhop to achieve any one of
#     several different goals, or to achieve them in some desired sequence.
#
# (4) Unlike SHOP and JSHOP, Pyhop does not include a Horn-clause inference
#     engine for evaluating preconditions of operators and methods. So far,
#     I have seen no need for it; I have found it easier to write precondition
#     evaluations directly in Python. But I could consider adding such a
#     feature if someone convinces me that it is really necessary.
#
# Accompanying this file are several files that give examples of how to use
# Pyhop. To run them, launch python and type "import blocks_world_examples"
# or "import simple_travel_example".


from __future__ import print_function
import copy,sys, pprint
import inspect
import traceback

############################################################
# States and goals

class State(object):
    """A state is just a collection of variable bindings."""
    def __init__(self,name):
        self.__name__ = name

class Goal(object):
    """A goal is just a collection of variable bindings."""
    def __init__(self,name):
        self.__name__ = name


### print_state and print_goal are identical except for the name

def print_state(state,indent=4):
    """Print each variable in state, indented by indent spaces."""
    if state != False:
        for (name,val) in vars(state).items():
            if name != '__name__':
                for x in range(indent): sys.stdout.write(' ')
                sys.stdout.write(state.__name__ + '.' + name)
                print(' =', val)
    else: print('False')

def print_goal(goal,indent=4):
    """Print each variable in goal, indented by indent spaces."""
    if goal != False:
        for (name,val) in vars(goal).items():
            if name != '__name__':
                for x in range(indent): sys.stdout.write(' ')
                sys.stdout.write(goal.__name__ + '.' + name)
                print(' =', val)
    else: print('False')

############################################################
# Helper functions that may be useful in domain models

def forall(seq,cond):
    """True if cond(x) holds for all x in seq, otherwise False."""
    for x in seq:
        if not cond(x): return False
    return True

def find_if(cond,seq):
    """
    Return the first x in seq such that cond(x) holds, if there is one.
    Otherwise return None.
    """
    for x in seq:
        if cond(x): return x
    return None

############################################################
# Commands to tell Pyhop what the operators and methods are

operators = {}
methods = {}

def declare_operators(*op_list):
    """
    Call this after defining the operators, to tell Pyhop what they are.
    op_list must be a list of functions, not strings.
    """
    operators.update({op.__name__:op for op in op_list})
    return operators

def declare_methods(task_name,*method_list):
    """
    Call this once for each task, to tell Pyhop what the methods are.
    task_name must be a string.
    method_list must be a list of functions, not strings.
    """
    methods.update({task_name:list(method_list)})
    return methods[task_name]

############################################################
# Commands to find out what the operators and methods are

def print_operators(olist=operators):
    """Print out the names of the operators"""
    print('OPERATORS:', ', '.join(olist))

def print_methods(mlist=methods):
    """Print out a table of what the methods are for each task"""
    print('{:<14}{}'.format('TASK:','METHODS:'))
    for task in mlist:
        print('{:<14}'.format(task) + ', '.join([f.__name__ for f in mlist[task]]))

############################################################
# The actual planner
import pdb
def pyhop(state, tasks, verbose=0):
    """
    Try to find a plan that accomplishes tasks in state.
    If successful, return the plan. Otherwise return False.
    """
    if verbose>0:
        msg = '** pyhop, verbose={}: **\n   state = {}\n   tasks = {}'
        msg = msg.format(verbose, state.__name__, tasks)
        print(msg)
    result = seek_plan(state,tasks,[],0,verbose)
    if verbose>0: print('** result =',result,'\n')
    return result

from pprint import pformat, pprint
def seek_plan(state,tasks,plan,depth,verbose=0):
    """
    Workhorse for pyhop. state and tasks are as in pyhop.
    - plan is the current partial plan.
    - depth is the recursion depth, for use in debugging
    - verbose is whether to print debugging messages
    """
    if depth > 100: sys.exit(0)

    if verbose > 1:
        print('\ndepth {} tasks:\n {}'.format(depth,"\n".join(map(str,tasks))))
        #print('\ndepth {} tasks:'.format(depth))#,pformat(tasks)))
        # for task in tasks:
        #     print(task)
        #     task_name = task[0]
        #     if not task_name in methods: continue
        #     for t in methods[task_name]:
        #         print(inspect.getcallargs(t, state, *task[1:]))
        #         print(inspect.getdoc(t))
        #         print(" ")
    if tasks == []:
        if verbose>2:
            print('depth {} returns plan {}'.format(depth,plan))
        return plan

    task1 = tasks[0]

    if task1[0] in operators:
        if verbose>2:
            print('depth {} action {}'.format(depth,task1))
        operator = operators[task1[0]]
        #print(task1)
        newstate = operator(copy.deepcopy(state),*task1[1:])
        if verbose>2:
            print('depth {} new state:'.format(depth))
            # pprint(newstate.object_at)
            # pprint(newstate.vehicle_at)
            #print_state(newstate)
        if newstate:
            solution = seek_plan(newstate,tasks[1:],plan+[task1],depth+1,verbose)
            if solution != False:
                return solution

    if task1[0] in methods:
        #if verbose>2: print('depth {} method instance {}'.format(depth,task1))
        relevant = methods[task1[0]]
        if verbose>2:
            print ("# relevant methods:",len(relevant))
        # queued_subtasks = []
        for n, method in enumerate(relevant):
            num_args = len(inspect.getargs(method.func_code)[0])
            # if improper number of args or preconds failed, skip this method
            subtasks = (method(state, *task1[1:]) if len(task1) == num_args else False)
            # try:
            #     subtasks = (method(state, *task1[1:]) if len(task1) == num_args else False)
            # except:
            #     exc_type, exc_value, exc_traceback = sys.exc_info()
            #     tb = traceback.extract_tb(exc_traceback)[-1]  # file, line_no of error, func_name, line string
            #     error_line_no = tb[1]
            #     lines, starting_line_no = inspect.getsourcelines(method)
            #     lines = "".join(lines[:error_line_no-starting_line_no+1])
            #     print("#FWE")
            #     print(tb)
            #     print(tb[0], tb[2])
            #     print(lines)
            #     print("")
            #     subtasks = False
            # queued_subtasks.append(subtasks)

            if subtasks == False and verbose > 3:
                print ("no subtasks for method {} of task '{}'".format(n, task1[0]))

            if subtasks == False: # continue only if subtasks False, not []!!
                continue

            subtask_strs = "\n\t".join(map(str, subtasks)) if subtasks else ""
            if verbose > 0:
                msg = "seeking plan on task {} method {}/{}"
                print(msg.format(method.func_name, n, len(relevant)))
                if subtask_strs:
                    print('\twith subtasks \n\t[{}]'.format(subtask_strs))
                print()

            solution = seek_plan(state, subtasks+tasks[1:], plan, depth+1, verbose)
            if solution != False:
                return solution


    if verbose>2:
        print('depth {} returns failure'.format(depth))
        # print(task1[0])
        # potentials = [operators[task1[0]]] if task1[0] in operators else methods[task1[0]]
        # for t in potentials:
        #     print(inspect.getcallargs(t, state, *task1[1:]))
        #     print(inspect.getdoc(t))
        #     print(" ")
        # print(" ")

    return False

def run(state, tasks, verbose=0, *args, **kwargs):
    if verbose > 0:
        print("Running planner PYHOP")

    if not(operators):
        raise Exception("no operators declared")
    if not(methods):
        raise Exception("no methods declared")

    return pyhop(state, tasks, verbose)
