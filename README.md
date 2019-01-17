# **Malmo Task Learning**

This repository contains functionality used in conjunction with Microsoft's MalmoPlatform (https://github.com/Microsoft/malmo) to support research into companion AI in a Minecraft environment. Through the use of hierarchical task networks, the goal of this project is to get non-hardcoded agents to develop a plan and perform the same complex tasks as agents who were hardcoded with what to do in their environments. This pipeline is as follows:

Run a hardcoded mission --> Produce training data --> Train HTN --> Use HTN on non-hardcoded agent

## **Setup**

- First, ensure that you have a working build of Microsoft's MalmoPlatform. The repository for the Malmo project can be found [here](https://github.com/Microsoft/malmo). Ensure that the 'launchClient' program runs and successfully produces a Minecraft client.

- Clone this repository onto your local machine at any location.

## **Project Pipeline**

### **I. Running Hardcoded Missions**

Hardcoded mission scripts designed for untrained agents are denoted by the '.mission' and '.UT' portions of the file name. All missions require two instances of the MalmoPlatform Minecraft client to be running. Executing one of these scripts will produce an execution trace log useful for training an HTN, as well as a performance stats file for each Agent. A mission can be ran like so:

    python3 malmo-task-learning/lib/<mission>

If you would like to run a single mission any number of times in a repeated fashion, you can also use the following command:

    python malmo-task-learning/lib/Run.py <mission> <# times>

### **II. Cleaning Up Execution Traces**

After running a single mission several times, there will be corresponding execution trace files in the logs/ directory. Due to the occasional tolerance and timing issues in using the MalmoPlatform, these files must be cleaned up before being used for training. To clean all files in the logs/ directory, run the following command:

    python malmo-task-learning/lib/ProcessLogs.py

### **III. Train a Hierarchical Task Network**

With the cleaned up execution trace files from step 2, an HTN can be trained to recognize parts of the environment from a mission and generate a plan of actions for new environments.

### **IV. Test the Trained Hierarchical Task Network**

After training the HTN in step 3 for a particular mission, the corresponding mission with filename extension '.T' can be ran. The agent for this mission is not hardcoded in the ways it responds to its environment, and is instead developing a plan each time it inspects the surroundings. Similarly to step 1, these missions can be ran like so:

    python malmo-task-learning/lib/<mission>

### **V. Evaluate Performance**

In order to better assess how a hardcoded or non-hardcoded agent performed, statistical information on each agent is automatically output in CSV format to the stats/ directory on each run of a mission. This can be read as plaintext, or can be graphed by running the following command:

    python malmo-task-learning/lib/Stats.py <CSV filename>

Running this script will ask the user for all of the attributes they wish to plot against the time that the mission ran for.