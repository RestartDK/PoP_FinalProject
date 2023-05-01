# room.py
# This file contains the room class of each room that will be put
# in the labyrinth

class Room:
    def __init__(self, name, items, chests, traps, exit_x, exit_y, width, height):
        self.name = name
        self.items = items
        self.chests = chests
        self.traps = traps
        self.exit_x = exit_x
        self.exit_y = exit_y
        self.width = width
        self.height = height
        

    # Getter methods
    def getName(self):
        return self.name

    def getItems(self):
        return self.items
    
    def getChests(self):
        return self.chests
    
    def getTraps(self):
        return self.traps
    
    def getWidth(self) -> int:
        return self.width
    
    def getHeight(self) -> int:
        return self.height
    
    def getExit_X(self):
        return self.exit_x
    
    def getExit_Y(self):
        return self.exit_y
    
    # Setter methods
    def setName(self, name):
        self.name = name

    def setItems(self, items):
        self.items = items
    
    def setChests(self, chests):
        self.chests = chests
    
    def setScore(self, traps):
        self.traps = traps
    
    def setWidth(self, width):
        self.width = width
    
    def setHeight(self, height):
        self.height = height
        
    def setExit_X(self, exit_x):
        self.exit_x = exit_x
        
    def setExit_Y(self, exit_y):
        self.exit_y = exit_y