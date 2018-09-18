# ==============================================================================================
# This file exposes functionality for logging traces containing both state and action
# information of a particular agent at regular intervals.
# ==============================================================================================
from datetime import datetime
import time

class Logger: {
    """
    Purely static class containing functionality for logging JSON traces containing state and action information
    as a result of some action performed by the companion. All of the methods in this class should be called
    from a corresponding action method, such that the trace output is produced as a direct result of performing
    an action.
    """
    contents = ""

    @staticmethod
    def __getTime__():
        """
        Internal method for getting a string containing the current time and date.
        """
        return datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')

    @staticmethod
    def __addLog__(s, observations):
        """
        Internal method for finalizing a log output with player and observation information
        and appending it to the running log.
        """
        contents += s + """
            "player": {},
            "inventory": {}
        }
        """.format(___________________________)

    @staticmethod
    def logAttack(targetBlockType, targetLocation, observations):
        """
        Add trace output resulting from an attack to the running log.
        """
        s = """{
            "time": {},
            "type": "attack",
            "target": {},
            "location": [{}, {}, {}],
        """.format(__getTime__(), targetBlockType.value, targetLocation[0], targetLocation[1], targetLocation[2])
        __addLog__(s, observations)

    @staticmethod
    def logPosition(position, observations):
        """
        Add trace output resulting from a position observation to the running log.
        """
        s = """{
            "time": {},
            "type": "position",
            "location": [{}, {}, {}],
        """.format(__getTime__(), position[0], position[1], position[2])
        __addLog__(s, observations)

    @staticmethod
    def logCrafting(item, ingredients, observations):
        """
        Add trace output resulting from crafting an item to the running log.
        """
        s = """{
            "time": {},
            "type": "crafting",
            "item": {},
            "ingredients": {},
        """.format(__getTime__(), item.value, __________)
        __addLog__(s, observations)

    @staticmethod
    def logMoveTo(targetBlockType, targetLocation, observations):
        """
        Add trace output resulting from moving to a specific block to the running log.
        """
        s = """{
            "time": {},
            "type": "moveto",
            "target": {},
            "location": [{}, {}, {}],
        """.format(__getTime__(), targetBlockType.value, targetLocation[0], targetLocation[1], targetLocation[2])
        __addLog__(s, observations)
}