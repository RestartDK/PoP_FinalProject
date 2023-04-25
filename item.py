# item.py
# This file contains the item class for each item that will be picked up in the game
# in game

class Item:
    def __init__(self, name, rarity, x_coordinate, y_coordinate, width, height):
        self.name = name
        self.rarity = rarity
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.width = width
        self.height = height

    # Returns the points value for the item
    def rarityPoints(self) -> int:
        # Rarity with corresponding points
        rarity_points = {
            "Common": 10,
            "Rare": 30,
            "Epic": 70,
            "Legendary": 150
        }
        return rarity_points[self.rarity]

    # Getter methods
    def getName(self) -> str:
        return self.name

    def getRarity(self) -> str:
        return self.rarity
    
    def getX_Coordinate(self) -> int:
        return self.x_coordinate
    
    def getY_Coordinate(self) -> int:
        return self.y_coordinate
    
    def getWidth(self) -> int:
        return self.width
    
    def getHeight(self) -> int:
        return self.height
    
     # Setter methods
    def setX_Coordinate(self, x_coordinate):
        self.x_coordinate = x_coordinate
        
    def setY_Coordinate(self, y_coordinate):
        self.y_coordinate = y_coordinate
        
    def setWidth(self, width):
        self.width = width
    
    def setHeight(self, height):
        self.height = height
    
    

    

    

    
    



    

    
        