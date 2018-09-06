# Malmo Task Learning

This repository is designed to help support research into companion AI in Minecraft. More specifically, the goal is to run a simulation with an automated player and companion, where the companion performs a hard-coded task. As the companion performs said tasks, we log the environment states and actions to a learning algorithm which attempts to classify complex tasks from a series of primitive tasks. Given a new companion that is NOT hardcoded, they should be able to use the "learned" model to perform the same task with similar performance.

## Contents

#### scenarios/

This directory contains Python scripts, each one representing a unique hardcoded scenario for both the player and the companion. The scenarios can be ran just like any other missions included in the original Malmo project. When running these scripts, the output traces will be fed to the learning algorithm to be used by future non-hardcoded companions.

#### tools/

This directory contains Python scripts that serve as tools for the development and runtime output of newly-created scenarios. These files should not be ran directly, but rather expose functions that other scripts can make use of.

## Usage

To make use of the scripts in this directory, clone this repository into your local copy of the Malmo platform at the following location:

```
MalmoPlatform/Python_Examples/
```

Now, just as you would run any of the original Python missions, you can run any of the scenarios at:

```
MalmoPlatform/Python_Examples/malmo-task-learning/
```