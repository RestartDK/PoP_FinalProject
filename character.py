# character.py
# This file contains the character class of the playable character
# in game

from item import Item
import pygame

class Character:
    def __init__(self, name, health, inventory, score, x_coordinate, 
                 y_coordinate, width, height):
        self.name = name
        self.health = health
        self.inventory = inventory
        self.score = score
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.width = width
        self.height = height

    # Update character's position based on elapsed time
    def update(self, keys_pressed, SCREEN_WIDTH, SCREEN_HEIGHT):
        if keys_pressed[pygame.K_w]:
            self.y_coordinate -= 1
        if keys_pressed[pygame.K_s]:
            self.y_coordinate += 1
        if keys_pressed[pygame.K_a]:
            self.x_coordinate -= 1
        if keys_pressed[pygame.K_d]:
            self.x_coordinate += 1
            
        # Adjust character's position to stay within screen boundaries
        if self.x_coordinate < 0:
            self.x_coordinate = 0
        if self.x_coordinate > SCREEN_WIDTH - self.width:
            self.x_coordinate = SCREEN_WIDTH - self.width
        if self.y_coordinate < 0:
            self.y_coordinate = 0
        if self.y_coordinate > SCREEN_HEIGHT - self.height:
            self.y_coordinate = SCREEN_HEIGHT - self.height
    
    # Draw the character on the screen 
    def draw(self, surface):
        pass
    
    # The puzzle of the game, returns true if the character has 3 legendary
    # items       
    def checkEasterEgg(self) -> bool:
        inventory = self.getInventory()
        legendaries = []
        for item in inventory:
            if len(legendaries) == 3: return True
            if item.getRarity() == "Legendary":
                legendaries.append(item)
        
        return False
    
    # Checks to see if chosen item exits in character inventory
    def findItemInInventory(self, chosen: str) -> Item:
        inventory = self.getInventory()
        for item in inventory:
            if chosen.lower() == item.getName().lower():
                return item
        
        raise ValueError("Item does not exist")
    
    # Looks through all rarity values of items in inventory and adjusts score
    def changeScore(self):
        inventory = self.inventory
        score = 0
        for item in inventory:
            score += item.rarityPoints()
        self.setScore(score)
            
    # Add item to inventory
    def addItem(self, item):
        self.inventory.append(item)

    # Remove item from inventory
    def removeItem(self, item):
        self.inventory.remove(item)

    # Remove damage for player health bar
    def removeHealth(self, num):
        self.setHealth(self.getHealth() - num)

    # Getter methods
    def getName(self) -> str:
        return self.name

    def getHealth(self) -> int:
        return self.health
    
    def getInventory(self):
        return self.inventory
    
    def getScore(self) -> int:
        return self.score
    
    def getX_Coordinate(self) -> int:
        return self.x_coordinate
    
    def getY_Coordinate(self) -> int:
        return self.y_coordinate
    
    def getWidth(self) -> int:
        return self.width
    
    def getHeight(self) -> int:
        return self.height
    
    # Setter methods
    def setName(self, name):
        self.name = name

    def setHealth(self, health):
        self.health = health
    
    def setInventory(self, inventory):
        self.inventory = inventory
    
    def setScore(self, score):
        self.score = score
    
    def setX_Coordinate(self, x_coordinate):
        self.x_coordinate = x_coordinate
        
    def setY_Coordinate(self, y_coordinate):
        self.y_coordinate = y_coordinate
        
    def setWidth(self, width):
        self.width = width
    
    def setHeight(self, height):
        self.height = height


    

