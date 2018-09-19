# ==============================================================================================
# This file exposes functionality for logging traces containing both state and action
# information of a particular agent at regular intervals.
# ==============================================================================================
from datetime import datetime
import os
import time
import json

class Logger:
    """
    Purely static class containing functionality for logging JSON traces containing state and action information
    as a result of some action performed by the companion. All of the methods in this class should be called
    from a corresponding action method, such that the trace output is produced as a direct result of performing
    an action.
    """
    __contents = "["

    @staticmethod
    def clear():
        """
        Clear the contents of this log.
        """
        Logger.__contents = "["

    @staticmethod
    def __getTime__():
        """
        Internal method for getting a string containing the current time and date.
        """
        return datetime.fromtimestamp(time.time()).strftime('%m-%d-%Y %H:%M:%S.%f')

    @staticmethod
    def logAttack(targetBlockType, targetLocation, observations):
        """
        Add trace output resulting from an attack to the running log.
        """
        Logger.__contents += '''{{
            "time": "{}",
            "type": "attack",
            "target": {},
            "location": [{}, {}, {}],
            "agent": {}
        }},'''.format(Logger.__getTime__(), targetBlockType.value, targetLocation[0], targetLocation[1], targetLocation[2], observations)

    @staticmethod
    def logPosition(observations):
        """
        Add trace output resulting from a position observation to the running log.
        """
        Logger.__contents += '''{{
            "time": "{}",
            "type": "position",
            "agent": {}
        }},'''.format(Logger.__getTime__(), observations)

    @staticmethod
    def logCrafting(item, ingredients, observations):
        """
        Add trace output resulting from crafting an item to the running log.
        """
        Logger.__contents += '''{{
            "time": "{}",
            "type": "crafting",
            "item": {},
            "ingredients": {},
            "agent": {}
        }},'''.format(Logger.__getTime__(), item.value, ___, observations)

    @staticmethod
    def logMoveTo(targetBlockType, targetLocation, observations):
        """
        Add trace output resulting from moving to a specific block to the running log.
        """
        Logger.__contents += '''{{
            "time": "{}",
            "type": "moveto",
            "target": {},
            "location": [{}, {}, {}],
            "agent": {}
        }},'''.format(Logger.__getTime__(), targetBlockType.value, targetLocation[0], targetLocation[1], targetLocation[2], observations)

    @staticmethod
    def flushToFile():
        """
        Outputs the current JSON log string to a file located a the 'logs' directory within the current working
        directory. The file name is determined by the current date and time.
        """
        Logger.__contents += "]"
        fileName = datetime.fromtimestamp(time.time()).strftime('%m_%d_%Y_%H_%M_%S') + "_log.json"
        filePath = "logs"
        if not os.path.isdir(filePath):
            os.mkdir(filePath)
        filePath = os.path.join(filePath, fileName)
        logFile = open(filePath, "w+")
        logFile.write(Logger.__contents)
        logFile.close()
        Logger.clear()
