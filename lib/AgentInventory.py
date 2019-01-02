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
    Item IDs at the FRONT of each array are the next to be used for items where the agent has more than one.
    """
    __idCounter__ = 0   # Used to uniquely identify items in a mission
    __idQueue__ = {}    # Map of item types to a list of ids of items that have been discovered but not yet picked up (the first item is the most recently identified "closest")

    def __init__(self):
        self.__inventory__ = {}

    def getId(self):
        """
        Returns a unique number that can be used to identify a new item in the inventory
        """
        AgentInventory.__idCounter__ += 1
        return AgentInventory.__idCounter__

    def update(self, agent):
        """
        Given an agent's inventory JSON from an observation, update this inventory to contain only the items found.
        """
        inventoryJson = agent.getInventoryJson()
        itemsLeft = len(inventoryJson) != 0
        while (itemsLeft):
            itemType = inventoryJson[0]["type"]
            numOfItemInObs = inventoryJson[0]["quantity"]
            if itemType not in self.__inventory__:  # Add an array of ids for this item type if it was never discovered
                self.__inventory__[itemType] = []
            numOfItemInInv = len(self.__inventory__[itemType])

            for i in range(1, len(inventoryJson)):  # Loop over remaining items, and for each item of matching type, add to counter
                if inventoryJson[i]["type"] == itemType:
                    numOfItemInObs += inventoryJson[i]["quantity"]
            inventoryJson = [item for item in inventoryJson if item["type"] != itemType] # Remove all of those inventory items
            
            if numOfItemInObs > numOfItemInInv: # Add more items with unique id of this type to inventory
                for i in range(numOfItemInInv, numOfItemInObs):
                    self.addItem(agent, itemType)  # This item was obtained not through action... needs id
            elif numOfItemInObs < numOfItemInInv: # Remove some items of this type from inventory
                for i in range(numOfItemInObs, numOfItemInInv):
                    if len(self.__inventory__[itemType]) > 0:
                        self.__inventory__[itemType].pop(0)

            # Only perform another iteration if there are more items of different types that we have not yet checked
            if len(inventoryJson) == 0:
                itemsLeft = False

    @staticmethod
    def enqueueItemId(item):
        """
        Places the id of an item that is closest to an agent in a queue such that when an item of that type is
        randomly added to the agent's inventory from a pick-up, we first select that id.
        """
        if item.type not in AgentInventory.__idQueue__:
            AgentInventory.__idQueue__[item.type] = []

        # If item id is already in queue, move it to front. Otherwise, just prepend it
        if item.id in AgentInventory.__idQueue__[item.type]:
            idx = AgentInventory.__idQueue__[item.type].index(item.id)
            del AgentInventory.__idQueue__[item.type][idx]
            AgentInventory.__idQueue__[item.type].insert(0, item.id)
        else:
            AgentInventory.__idQueue__[item.type].insert(0, item.id)

    @staticmethod
    def dequeueItemId(itemTypeStr):
        """
        Removes the first item id of a specific type from the queue.
        """
        if itemTypeStr not in AgentInventory.__idQueue__:
            return
        if len(AgentInventory.__idQueue__[itemTypeStr]) <= 0:
            return
        AgentInventory.__idQueue__[itemTypeStr].pop(0)

    def addItem(self, agent, itemTypeStr, itemId = None):
        """
        Add an item of a specific type to this inventory, given the type as a string.
        If no item ID was given, the ID will be either pulled from a queue or generated.
        """
        if itemTypeStr not in self.__inventory__:
            self.__inventory__[itemTypeStr] = []
        if itemId == None:
            if itemTypeStr in AgentInventory.__idQueue__ and len(AgentInventory.__idQueue__[itemTypeStr]) > 0:
                itemId = AgentInventory.__idQueue__[itemTypeStr][0]
                self.dequeueItemId(itemTypeStr)
            else:
                itemId = "{}{}".format(itemTypeStr, self.getId())
        item = Item(itemId, itemTypeStr)
        Logger.logAgentAquiredItem(agent, item)
        self.__inventory__[itemTypeStr].append(item)
        return item

    def removeItem(self, agent, item):
        """
        Removes an item with a specific id from this inventory.
        """
        if item.type not in self.__inventory__:
            return
        for i in range(0, len(self.__inventory__[item.type])):
            if self.__inventory__[item.type][i].id == item.id:
                self.__inventory__[item.type].pop(i)
                Logger.logAgentLostItem(agent, item)
                return

    def allItems(self, agent):
        """
        Returns a list of all of the items in this inventory.
        """
        items = []
        for itemType in self.__inventory__:
            for item in self.__inventory__[itemType]:
                items.append(item)
        return items

    def allItemsByType(self, agent, itemType):
        """
        Returns a list of all of the items in this inventory for a specific type.
        """
        if itemType.value not in self.__inventory__:
            return []
        return self.__inventory__[itemType.value]

    def itemByType(self, agent, itemType):
        """
        Returns an item in this inventory of a specific type. Returns None if no item for that type exists in this inventory.
        """
        if itemType.value not in self.__inventory__:
            return None
        if len(self.__inventory__[itemType.value]) == 0:
            return None
        return self.__inventory__[itemType.value][0]

    def amountOfItem(self, agent, item):
        """
        Returns the quantity of a type of item in this inventory.
        """
        if item.value not in self.__inventory__:
            return 0
        return len(self.__inventory__[item.value])

    def printOut(self, agent):
        """
        DEBUG ONLY
        """
        print("=========================================")
        for item in self.__inventory__:
            for itemId in self.__inventory__[item]:
                print(itemId)
        print("=========================================")