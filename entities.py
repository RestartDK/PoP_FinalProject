# labyrinth.py
# This file contains the class labyrinth. It will create the labyrinth
# With all the entities inside it (Character, Room, Chest, Trap, Item)
# Note that rarity chance is C:50%, R:30%, E:20%, L:10%
import random
from chest import Chest
from trap import Trap
from room import Room
from item import Item
from character import Character

# Raised when the rarity does not match in game
class RarityMatch(Exception):
    pass
    
# Had =None on each parameter
class Entities:
    def __init__(self, roomcount: int, ROOM_WIDTH, ROOM_HEIGHT, common_items=None, rare_items=None, 
                 epic_items=None, legendary_items=None):
        self.roomcount = roomcount
        self.common_items = common_items
        self.rare_items = rare_items
        self.epic_items = epic_items
        self.legendary_items = legendary_items
        self.ROOM_WIDTH = ROOM_WIDTH
        self.ROOM_HEIGHT = ROOM_HEIGHT

    # TODO: Change the file names to actual good pics
    # Creating all the items in the game
    def defineItems(self):
        paper = Item("Piece of paper", "Common", 30, 30, "assets/items/gold.png")
        rock = Item("Rock", "Common", 30, 30, "assets/items/gold.png")
        scissors = Item("Scissors", "Common", 30, 30, "assets/items/gold.png")
        silver = Item("Silver ingot", "Rare", 30, 30, "assets/items/gold.png")
        iron = Item("Iron ingot", "Rare", 30, 30, "assets/items/gold.png")
        copper = Item("Copper ingot", "Rare", 30, 30, "assets/items/gold.png")
        amulet = Item("Amulet", "Epic", 30, 30, "assets/items/gold.png")
        medalion = Item("Medalion", "Epic", 30, 30, "assets/items/gold.png")
        trophy = Item("Trophy", "Epic", 30, 30, "assets/items/gold.png")
        wand = Item("Wand", "Legendary", 30, 30, "assets/items/gold.png")
        emerald = Item("Emerald", "Legendary", 30, 30, "assets/items/gold.png")
        pandora = Item("Pandora's box", "Legendary", 30, 30, "assets/items/gold.png")

        # Sorting out the items into 3 different lists of rarity
        common_items = [paper, rock, scissors]
        rare_items = [silver, iron, copper]
        epic_items =[amulet, medalion, trophy]
        legendary_items = [wand, emerald, pandora]
        
        # Setting the items to the entities object
        self.setCommonItems(common_items)
        self.setRareItems(rare_items)
        self.setEpicItems(epic_items)
        self.setLegendaryItems(legendary_items)
        
        return common_items, rare_items, epic_items, legendary_items

    # Fuses 2 items in inventory, removes the 2 chosen items and chooses a random one in next rarity
    def fuseItems(self, item1: Item, item2: Item, character: Character):
        fuse_item = None
        
        if item1.getRarity() == "Common" and item2.getRarity() == "Common":
            character.removeItem(item1)
            character.removeItem(item2)
            items = self.getRareItems()
            fuse_item = items[random.randint(0, len(items)-1)]
            character.addItem(fuse_item)
        elif item1.getRarity() == "Rare" and item2.getRarity() == "Rarity":
            character.removeItem(item1)
            character.removeItem(item2)
            items = self.getEpicItems()
            fuse_item = items[random.randint(0, len(items)-1)]
            character.addItem(fuse_item)
        elif item1.getRarity() == "Epic" and item2.getRarity() == "Epic":
            character.removeItem(item1)
            character.removeItem(item2)
            items = self.getLegendaryItems()
            fuse_item = items[random.randint(0, len(items)-1)]
            character.addItem(fuse_item)
        else:
            raise RarityMatch("The Rarities do not match")

        # Changing score after fusion
        character.changeScore()
        return fuse_item
        
    # Method to create a chest with random chance to have epic or legendary
    def createChest(self, epic, legendary) -> Chest:
        choices = [epic, legendary]
        rarity = random.choices(choices, weights=(20, 10), k=1)
        
        # Rarity is returned as a list so as 2 choices we return element 0 and
        # rarity is a list of the n items in their rarity category so we choose
        # one item randomly with equal weighted probability
        items = rarity[0]
        item = items[random.randint(0, len(items)-1)]
        chest = Chest("chest", item, 30, 30)   

        return chest
    
    # Method to create trap with random chance of its size
    def createTrap(self) -> Trap:
        # Default trap size will only be width and length 2 - 4
        w = random.choice([2, 4])
        l = random.choice([2, 4])

        # Default damage for trap is 1 health for the character
        trap = Trap(1, 30, 30)

        return trap
    
    # Method to create n rooms in the labyrinth
    def createRooms(self, n, ROOM_WIDTH, ROOM_HEIGHT, maxChests, maxTraps, maxItems):
        # Invoking all the items in the game
        common_items, rare_items, epic_items, legendary_items = self.defineItems()
        all_items = [common_items, rare_items, epic_items, legendary_items]
        
        # Generating entities for n rooms
        rooms = []
        for i in range(n):

            # Making 0 - 3 chests with random items inside
            chests = []
            for j in range(random.randint(0, maxChests)):
                chests.append(self.createChest(epic_items, legendary_items))
                
            #print(chests[0].getName())
            
            # Making 0 - 3 traps with random width and length of max values 2 or 4
            traps = []
            for j in range(random.randint(0, maxTraps)):
                traps.append(self.createTrap())

            # Choosing 0 - 4 items with respective weightings
            items = []
            rarities = random.choices(all_items, weights=(50, 30, 20, 10), k=maxItems)

            # Made a list of all items with their rarity, now take a random item from 
            # rarity category with equal weighting
            for item in rarities:
                items.append(item[random.randint(0, len(item)-1)])

            # Creating Room object with all entities
            exit_x = int(ROOM_WIDTH/2)
            exit_y = int(ROOM_HEIGHT/2)
            room = Room("Room" + str(i), items, chests, traps, exit_x, exit_y, ROOM_WIDTH, ROOM_HEIGHT)
            rooms.append(room)

        return rooms
    
    # Place all chosen type of entity on the boundries of each room
    def placeEntityType(self, entities, room: Room):
        for entity in entities:
            boundary_x = room.getWidth()
            boundary_y = room.getHeight()
            position_new_x = random.randint(0, boundary_x)
            position_new_y = random.randint(0, boundary_y)
            entity.setX_Coordinate(position_new_x)
            entity.setY_Coordinate(position_new_y)
        
    # Places all entities randomly in boundaries of the room
    def placeAllEntities(self, rooms):
        for room in rooms:
            items = room.getItems()
            chests = room.getChests()
            traps = room.getTraps()
            self.placeEntityType(items, room)
            self.placeEntityType(chests, room)
            self.placeEntityType(traps, room)

    # Create full labyrinth with n rooms
    def createLabyrinth(self):
        rooms = self.createRooms(self.getRoomCount(), self.ROOM_WIDTH, self.ROOM_HEIGHT, maxChests=3, maxTraps=3, maxItems=4)
        self.placeAllEntities(rooms)

        return rooms
    
    # Getter methods
    def getRoomCount(self) -> int:
        return self.roomcount

    def getCommonItems(self):
        return self.common_items
    
    def getRareItems(self):
        return self.rare_items
    
    def getEpicItems(self):
        return self.epic_items
    
    def getLegendaryItems(self):
        return self.legendary_items
    
    # Setter methods
    def setRoomCount(self, roomcount):
        self.roomcount = roomcount
    
    def setCommonItems(self, common_items):
        self.common_items = common_items
    
    def setRareItems(self, rare_items):
        self.rare_items = rare_items
        
    def setEpicItems(self, epic_items):
        self.epic_items = epic_items
        
    def setLegendaryItems(self, legendary_items):
        self.legendary_items = legendary_items
    

