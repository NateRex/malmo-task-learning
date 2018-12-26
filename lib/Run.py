# ==============================================================================================
# This file represents a standalone script for running one of the missions in this directory
# a certain number of times contiguously. This is useful for exhaustively simulating a single
# mission.
# ==============================================================================================
import os
import sys
import subprocess

def main():
    if len(sys.argv) < 3:
        print("Usage: Run.py <mission> <times>")
        return

    missionFile = os.path.join(os.getcwd(), sys.argv[1])
    numberOfRuns = int(sys.argv[2])

    if not os.path.isfile(missionFile):
        print("Could not find mission script '{}'".format(missionFile))
        return

    for i in range(0, numberOfRuns):
        print("Starting run {}".format(i + 1))
        subprocess.check_output(["python3", missionFile], shell=True)

    print("Done")

if __name__ == "__main__":
    main()