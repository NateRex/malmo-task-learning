# ==============================================================================================
# This file holds the AgentInventory class for dynamically storing the items held by a player,
# along with corresponding ids used when generating log traces.
# ==============================================================================================
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
                    self.__inventory__[itemType].append("{}{}".format(itemType, self.__getId__()))
            elif numOfItemInObs < numOfItemInInv: # Remove some items of this type from inventory
                for i in range(numOfItemInObs, numOfItemInInv):
                    if len(self.__inventory__[itemType]) > 0:
                        self.__inventory__[itemType].pop(0)

            # Only perform another iteration if there are more items of different types that we have not yet checked
            if len(inventory) == 0:
                itemsLeft = False

    def addItem(self, item):
        """
        Add an item of a specific type to this inventory. Returns the id of the item added.
        """
        if item.value not in self.__inventory__:
            self.__inventory__[item.value] = []
        itemId = "{}{}".format(item.value, self.__getId__())
        self.__inventory__[item.value].append(itemId)
        return itemId

    def removeItem(self, item, itemId):
        """
        Removes an item of a specific type and id from this inventory.
        """
        if item.value not in self.__inventory__:
            return
        self.__inventory__[item.value].remove(itemId)

    def getAllItemIds(self):
        """
        Returns a list of all of the item ids in this inventory.
        """
        itemIds = []
        for itemType in self.__inventory__:
            for itemId in self.__inventory__[itemType]:
                itemIds.append(itemId)
        return itemIds

    def getItemTypeIds(self, item):
        """
        Returns a list of item ids currently in this inventory for a specific item type.
        """
        if item.value not in self.__inventory__:
            return []
        return self.__inventory__[item.value]

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