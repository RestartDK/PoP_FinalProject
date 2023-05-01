# frontend.py
# This file contains the front end classes of the whole application

import pygame
from character import Character
from chest import Chest
from room import Room
from trap import Trap
from item import Item

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class FrontEndCharacter(pygame.sprite.Sprite):
    def __init__(self, picture_path, character: Character):
        super().__init__()
        self.character = character
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (character.getWidth(), character.getHeight())) 
        self.rect = self.image.get_rect()
        self.rect.x = character.getX_Coordinate()
        self.rect.y = character.getY_Coordinate()
        
    # Move the sprite based on user keypresses
    def update(self):
        self.rect.x = self.character.getX_Coordinate()
        self.rect.y = self.character.getY_Coordinate()
            
    def optionalCollisions(self, chest_sprites, item_sprites):
        collided_chests = pygame.sprite.spritecollide(self, chest_sprites, False)
        if collided_chests:
            for front_end_chest in collided_chests:
                chest = front_end_chest.entity
                self.openChest(chest)

        collided_items = pygame.sprite.spritecollide(self, item_sprites, True)
        if collided_items:
            for front_end_item in collided_items:
                item = front_end_item.entity
                self.pickUpItem(item)
    
    def mandatoryCollisions(self, trap_sprites, exit_sprites, game_state, game):
        collided_traps = pygame.sprite.spritecollide(self, trap_sprites, False)
        if collided_traps:
            for front_end_trap in collided_traps:
                trap = front_end_trap.entity
                self.stepTrap(trap)
        
        collided_exit = pygame.sprite.spritecollide(self, exit_sprites, False)    
        if collided_exit and not game.room_change:
            game.room_change = True
            game_state.state = "changeRoom"
            
                
        
    def openChest(self, chest: Chest):
        item = chest.getItem()
        if item != None:
                self.character.addItem(item)
                # Updating score with new item
                self.character.changeScore()
                
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print("You just picked up: ", chest.getItem().getName(), " (", chest.getItem().getRarity(), ")")
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print()
                chest.setItem(None)
    
    def pickUpItem(self, item: Item):
        self.character.addItem(item)    
        # Updating score with new item
        self.character.changeScore()
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("You just picked up: ", item.getName(), " (", item.getRarity(), ")")
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    
    def stepTrap(self, trap: Trap):
        damage = trap.getDamage()
        self.character.removeHealth(damage)
        print("")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Oh no you have walked into a trap and you have been damaged by 1 heart!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("")

class FrontEndExit(pygame.sprite.Sprite):
    def __init__(self, picture_path, room: Room):
        super().__init__()
        self.room = room
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = room.getExit_X()
        self.rect.y = room.getExit_Y()
        
    def update(self):
        self.rect.x = self.entity.getExit_X()
        self.rect.y = self.entity.getExit_Y()
    
# Frontend class for all types of entities    
class FrontEndEntity(pygame.sprite.Sprite):
    def __init__(self, picture_path, entity):
        super().__init__()
        self.entity = entity
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (entity.getWidth(), entity.getHeight()))
        self.rect = self.image.get_rect()
        self.rect.x = entity.getX_Coordinate()
        self.rect.y = entity.getY_Coordinate()
        
    def update(self):
        self.rect.x = self.entity.getX_Coordinate()
        self.rect.y = self.entity.getY_Coordinate()
    
class FrontEndGameover(pygame.sprite.Sprite):
    def __init__(self, exit_path, replay_path, score, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__()
        self.image = pygame.image.load(exit_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT/2))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.score = score
        self.font = pygame.font.SysFont("monospace", 36)
        self.score_label = self.font.render("Final Score: " + str(score), 1, (128, 128, 128))
        self.replay_button = pygame.image.load(replay_path).convert_alpha()
        self.replay_button = pygame.transform.scale(self.replay_button, (150, 75))
        self.replay_button_rect = self.replay_button.get_rect()
        self.replay_button_rect.x = SCREEN_WIDTH/2 - 75
        self.replay_button_rect.y = SCREEN_HEIGHT/2 + 100
        
    def updateScoreLabel(self, score):
        self.score_label = self.font.render("Final Score: " + str(score), 1, (255, 255, 255))
    
        
    def setScore(self, score):
        self.score = score
