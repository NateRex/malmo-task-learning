# Malmo Task Learning

This repository is designed to help support research into companion AI in Minecraft. More specifically, the goal is to run a simulation with an automated player and companion, where the companion performs a hard-coded task. As the companion performs said tasks, we log the environment states and actions to a learning algorithm which attempts to classify complex tasks from a series of primitive tasks. Given a new companion that is NOT hardcoded, they should be able to use the "learned" model to perform the same task with similar performance.

## Usage

- First, ensure that you have a working copy of Microsoft's MalmoPlatform, and can run both the Minecraft client and the Python missions. The repository for the Malmo project can be found [here](https://github.com/Microsoft/malmo).

- Clone this repository onto your local machine. Since this repository contains copies of the shared object libraries and MalmoPlatform interfaces that Microsoft's missions use to run, the location of the repo on your machine is not important. The missions should be runnable from anywhere.

- Ensure that you have a sufficient number of Malmo Minecraft clients running for a particular mission, and then run any of the missions using the following command as an example:

    ```
    python malmo-task-learning/lib/Example.mission.py
    ```

## Contents

#### lib/

This directory contains Python scripts representing unique hardcoded scenarios for players agents and their companions. A scenario can be ran just like any other Python example mission included in the default clone of the Malmo project. When running these scripts, the trace outputs will be fed to the learning algorithm to be used by future non-hardcoded companions.

There are also several Python scripts that serve as tools for the development of scenarios. These files should **NOT** be ran directly, but rather they expose functionality that the scenario scripts can make use of. These are listed below:

- **Constants**: Enumerated types for specifying certain characteristics of the environment, such as block type, item type, direction, time of day, etc.

- **ScenarioBuilder**: Functionality for dynamically building up the XML string representations of a scenario, including both agent and environment settings.

- **Logger**: Functionality for outputting the generated traces of a scenario as it is ran, which includes both state and action contents.

- **MalmoPython**: A copy of Microsoft's shared object library containing the Malmo interface, callable from Python.

- **malmoutils**: A copy of Microsoft's Python script which includes utility functions and classes that provide additional support for working with the Malmo interface.