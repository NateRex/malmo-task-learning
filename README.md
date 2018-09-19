# Malmo Task Learning

This repository is designed to help support research into companion AI in Minecraft. More specifically, the goal is to run a simulation with an automated player and companion, where the companion performs a hard-coded task. As the companion performs said tasks, we log the environment states and actions to a learning algorithm which attempts to classify complex tasks from a series of primitive tasks. Given a new companion that is NOT hardcoded, they should be able to use the "learned" model to perform the same task with similar performance.

## Contents

#### lib/

This directory contains Python scripts representing unique hardcoded scenarios for players agents and their companions. A scenario can be ran just like any other Python example mission included in the default clone of the Malmo project. When running these scripts, the trace outputs will be fed to the learning algorithm to be used by future non-hardcoded companions.

There are also several Python scripts that serve as tools for the development of scenarios. These files should **NOT** be ran directly, but rather they expose functionality that the scenario scripts can make use of. These are listed below:

- **ScenarioBuilder**: Functionality for dynamically building up the XML string representations of a scenario, including both agent and environment settings.

- **TraceLogger**: Functionality for outputting the generated traces of a scenario as it is ran, which includes both state and action contents.

## Usage

First, ensure that you have a working copy of Microsoft's MalmoPlatform, and can run both the Minecraft client and the Python missions. The repository for the Malmo project can be found [here](https://github.com/Microsoft/malmo). Once that is working, clone this repository onto your local machine at any location.

#### Windows

- Add the Python_Examples/ directory of the MalmoPlatform repository to your list of environment variables.

- Any of the missions in this repository can then be ran using Python:

    ```
    cd .../malmo-task-learning/lib/
    python Example.mission.py
    ```

#### Mac/Linux

- Add the Python_Examples/ directory to the PYTHONPATH environment variable in either .bash_profile or .bash_src:

    ```
    export PYTHONPATH=..../MalmoPlatform/Python_Examples:$PYTHONPATH
    ```

- Any of the missions in this repository can then be ran using Python:

    ```
    cd .../malmo-task-learning/lib/
    sudo python Example.mission.py
    ```