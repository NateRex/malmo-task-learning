# ==============================================================================================
# This file holds the AgentInventory class for dynamically storing the items held by a player,
# along with corresponding ids used when generating log traces.
# ==============================================================================================
from Utils import *
from Logger import *

class AgentInventory:
    """
    Class containing all of the inventory items an Agent is currently in possession of.
    This inventory object must be updated at regular intervals when new JSON observations come in from the AgentHost.
    """
    idCounter = 0   # Used to uniquely identify all items during a mission

    def __init__(self):
        self.__inventory__ = {}

    def __getId__(self):
        """
        Returns a unique number that can be used to identify a new item in the inventory
        """
        AgentInventory.idCounter += 1
        return AgentInventory.idCounter

    def update(self, inventory):
        """
        Given an agent's inventory JSON from an observation, update this inventory to contain only the items found.
        """
        itemsLeft = len(inventory) != 0
        while (itemsLeft):
            itemType = inventory[0]["type"]
            numOfItemInObs = inventory[0]["quantity"]
            if itemType not in self.__inventory__:  # Add an array of ids for this item type if it was never discovered
                self.__inventory__[itemType] = []
            numOfItemInInv = len(self.__inventory__[itemType])

            for i in range(1, len(inventory)):  # Loop over remaining items, and for each item of matching type, add to counter
                if inventory[i]["type"] == itemType:
                    numOfItemInObs += inventory[i]["quantity"]
            inventory = [item for item in inventory if item["type"] != itemType] # Remove all of those inventory items
            
            if numOfItemInObs > numOfItemInInv: # Add more items with unique id of this type to inventory
                for i in range(numOfItemInInv, numOfItemInObs):
                    self.addItem(itemType)
            elif numOfItemInObs < numOfItemInInv: # Remove some items of this type from inventory
                for i in range(numOfItemInObs, numOfItemInInv):
                    if len(self.__inventory__[itemType]) > 0:
                        self.__inventory__[itemType].pop(0)

            # Only perform another iteration if there are more items of different types that we have not yet checked
            if len(inventory) == 0:
                itemsLeft = False

    def addItem(self, itemType, itemId = None):
        """
        Add an item of a specific type to this inventory. Returns the item.
        If the item already had an id, provide it to this method. Otherwise, a new
        global id for the item will be generated.
        """
        if itemType.value not in self.__inventory__:
            self.__inventory__[itemType.value] = []
        itemId = itemId if itemId != None else "{}{}".format(itemType.value, self.__getId__())
        item = Item(itemId, itemType.value)
        self.__inventory__[itemType.value].append(item)
        Logger.logNewItem(item) # Log the new item 'into existence'
        return item

    def removeItem(self, item):
        """
        Removes an item from this inventory.
        """
        if item.type not in self.__inventory__:
            return
        for i in range(0, len(self.__inventory__[item.type])):
            if self.__inventory__[item.type][i].id == item.id:
                self.__inventory__[item.type].pop(i)
                return

    def getAllItems(self):
        """
        Returns a list of all of the items in this inventory.
        """
        items = []
        for itemType in self.__inventory__:
            for item in self.__inventory__[itemType]:
                items.append(item)
        return items

    def getAllItemsOfType(self, itemType):
        """
        Returns a list of all of the items in this inventory for a specific type.
        """
        if itemType.value not in self.__inventory__:
            return []
        return self.__inventory__[itemType.value]

    def getItem(self, itemType):
        """
        Returns an item in this inventory of a specific type. Returns None if no item for that type exists in this inventory.
        """
        if itemType.value not in self.__inventory__:
            return None
        if len(self.__inventory__[itemType.value]) == 0:
            return None
        return self.__inventory__[itemType.value][0]

    def amountOfItem(self, item):
        """
        Returns the quantity of a type of item in this inventory.
        """
        if item.value not in self.__inventory__:
            return 0
        return len(self.__inventory__[item.value])

    def printOut(self):
        """
        DEBUG ONLY
        """
        for item in self.__inventory__:
            for itemId in self.__inventory__[item]:
                print(itemId)