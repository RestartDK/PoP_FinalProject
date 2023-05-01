# game.py
# This file contains the controller class of the application

import pygame, sys, time
from character import Character
from chest import Chest
from room import Room
from entities import Entities
from trap import Trap
from item import Item

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROOM_WIDTH = 400
ROOM_HEIGHT = 400

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
    
    def mandatoryCollisions(self, trap_sprites, exit_sprites, game_state):
        collided_traps = pygame.sprite.spritecollide(self, trap_sprites, False)
        if collided_traps:
            for front_end_trap in collided_traps:
                trap = front_end_trap.entity
                #collided_traps.remove(front_end_trap)
                self.stepTrap(trap)
        
        collided_exit = pygame.sprite.spritecollide(self, exit_sprites, True)    
        if collided_exit:
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
        print("You just picked up: ", item.getName())
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    
    def stepTrap(self, trap: Trap):
        damage = trap.getDamage()
        self.character.removeHealth(damage)
        print("")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Oh no you have walked into a trap and you have been damaged by 1 heart!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("")
        
class FrontEndRoom(pygame.sprite.Sprite):
    def __init__(self, picture_path, room: Room):
        super().__init__()
        self.room = room
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (room.getWidth(), room.getHeight()))
        self.rect = self.image.get_rect()
        self.rect.x = room.getX_Coordinate()
        self.rect.y = room.getY_Coordinate()
        

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
    def __init__(self, exit_path, replay_path, score):
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
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.score_label, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2))
        screen.blit(self.replay_button, self.replay_button_rect)
        
    def setScore(self, score):
        self.score = score

# TODO: Keep this here and move other methods to a frontend.py file
# Controller class to connect the frontend and backend
class Game():
    def __init__(self, entities: Entities, SCREEN_WIDTH: int, SCREEN_HEIGHT: int):
        pygame.init()
        self.labyrinth = entities.createLabyrinth()
        self.game_state = GameState(self)
        self.room_count = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.start_button = pygame.image.load("assets/buttons/start.png")
        self.background = pygame.image.load("assets/backgrounds/BG.jpeg").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.backend_character = Character("Bob", health=3, inventory=[], 
                                           score=0, x_coordinate=0, y_coordinate=0,
                                           width=50, height=50)
        self.frontend_character = FrontEndCharacter("assets/players/player.png", self.backend_character)
        self.player_sprites = pygame.sprite.Group()
        self.player_sprites.add(self.frontend_character)
        self.exit_sprites = pygame.sprite.Group()
        self.chest_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.trap_sprites = pygame.sprite.Group()
        self.gameover_screen = FrontEndGameover("assets/buttons/gameover.png", "assets/buttons/replay.png", self.backend_character.getScore())
        self.secretEnd_screen = FrontEndGameover("assets/buttons/crown.png", "assets/buttons/replay.png", self.backend_character.getScore())
        
    def handle_events(self):
        self.game_state.stateManager()
            
    def intro_events(self):
        self.backend_character.setHealth(3)
        self.backend_character.setScore(0)
        self.backend_character.setInventory([])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type ==  pygame.MOUSEBUTTONDOWN:
                self.labyrinth = entities.createLabyrinth()
                self.game_state.state = "changeRoom"
    
    def mainGame_events(self):
        # Updates the score label on the gameoverscreen
        self.gameover_screen.updateScoreLabel(self.backend_character.getScore())
        self.secretEnd_screen.updateScoreLabel(self.backend_character.getScore())
        
        # If there are no more rooms or character health is 0, end the game
        if self.room_count >= len(self.labyrinth) or self.backend_character.getHealth() < 0:
            self.game_state.state = "end"
            return
        if self.backend_character.checkEasterEgg() == True:
            self.game_state.state = "secretEnd"
            return
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_e:
                    self.frontend_character.optionalCollisions(self.chest_sprites, self.item_sprites)
        
        self.frontend_character.mandatoryCollisions(self.trap_sprites, self.exit_sprites, self.game_state)
        

    def changeRoom_events(self):  
        # Reset character position
        self.backend_character.setX_Coordinate(0)
        self.backend_character.setY_Coordinate(0)
        self.initialiseEntities(self.labyrinth[self.room_count])
        print("Room count: ", self.room_count)
        print("Total rooms: ", len(self.labyrinth))
        print("Player score: ", self.backend_character.getScore())
        
        # Increase room count to go to next room
        self.room_count += 1
        
        print("You are in Room: ", self.room_count)
        
        # Chane game state to go back to initialise new room
        self.game_state.state = "mainGame"
    
    def end_events(self):
        self.gameover_screen.setScore(self.backend_character.getScore())
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN or event.key == pygame.MOUSEBUTTONDOWN:
                    self.room_count = 0
                    self.game_state.state = "intro"
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.room_count = 0
                self.game_state.state = "intro"
    
    def secretEnd_events(self):
        self.gameover_screen.setScore(self.backend_character.getScore())
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    self.room_count = 0
                    self.game_state.state = "intro"
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.room_count = 0
                self.game_state.state = "intro"
                    
                
    def update(self):
        keys_pressed = pygame.key.get_pressed()
        self.backend_character.update(keys_pressed, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.frontend_character.update()
        
    def drawRoom(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.frontend_character.image, self.frontend_character.rect)
        self.chest_sprites.draw(self.screen)
        self.item_sprites.draw(self.screen)
        self.trap_sprites.draw(self.screen)
        self.exit_sprites.draw(self.screen)
        pygame.display.flip()
    
    def drawIntro(self):
        self.screen.fill((255, 255, 255))
        # Draw the background and start screen
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.start_button, (SCREEN_HEIGHT/2 - 130, SCREEN_WIDTH/2 - 200)) 
        pygame.display.flip()
        
    def drawEnd(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.gameover_screen.image, self.gameover_screen.rect)
        self.screen.blit(self.gameover_screen.score_label, (SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2))
        self.screen.blit(self.gameover_screen.replay_button, self.gameover_screen.replay_button_rect)
        pygame.display.flip()
    
    def drawSecretEnd(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.secretEnd_screen.image, self.secretEnd_screen.rect)
        self.screen.blit(self.secretEnd_screen.score_label, (SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2))
        self.screen.blit(self.secretEnd_screen.replay_button, self.secretEnd_screen.replay_button_rect)
        pygame.display.flip()
    
    def initialiseEntities(self, room):
        self.chest_sprites.empty()
        self.item_sprites.empty()
        self.trap_sprites.empty()
        self.exit_sprites.empty()
        self.createFrontEndItems(room)
        self.createFrontEndChests(room)
        self.createFrontEndTraps(room)
        self.createFrontEndExit(room)
    
    # Initialises all entities in given room with their respective frontend 
    # instance
    def createFrontEndItems(self, room: Room):
        items = room.getItems()
        for item in items:
            frontend_item = FrontEndEntity(item.getPicture_Path(), item)
            self.item_sprites.add(frontend_item)
    
    def createFrontEndChests(self, room: Room):
        chests = room.getChests()
        for chest in chests:
            frontend_chest = FrontEndEntity("assets/chests/chest.png", chest)
            self.chest_sprites.add(frontend_chest)
            
    def createFrontEndTraps(self, room: Room):
        traps = room.getTraps()
        for trap in traps:
            frontend_trap = FrontEndEntity("assets/traps/lava.png", trap)
            self.trap_sprites.add(frontend_trap)
    
    def createFrontEndExit(self, room:Room):
        frontend_exit = FrontEndExit("assets/exits/portal.png", room)
        self.exit_sprites.add(frontend_exit)
        

# State manager for handling different stages of the game  
class GameState():
    def __init__(self, game: Game):
        self.state = "intro"
        self.game = game
        
    def intro(self):
        # Handle intro events
        game.intro_events()
        
        # Draw everything
        game.drawIntro()

    def mainGame(self):
        # Handle room events
        game.mainGame_events()
        
        # Update game state
        game.update()
        
        # Draw the screen
        game.drawRoom()
        
    def changeRoom(self):
        # Handle changing room events
        game.changeRoom_events()
        
    def end(self):
        # Handle end game events
        game.end_events()
        
        # Draw the screen
        game.drawEnd()
        
    def secretEnd(self):
        # Handle secret end game events
        game.secretEnd_events()
        
        # Draw the screen
        game.drawSecretEnd()
        
    def stateManager(self):
        if self.state == "intro":
            self.intro()
        if self.state == "mainGame":
            self.mainGame() 
        if self.state == "changeRoom":
            self.changeRoom()
        if self.state == "end":
            self.end()
        if self.state == "secretEnd":
            self.secretEnd()
            
# TODO: Put this in run method
if __name__ == "__main__":
    #Initalise Game Object (controller)
    entities = Entities(5, SCREEN_WIDTH, SCREEN_HEIGHT)
        
    game = Game(entities, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        # Handle events
        game.handle_events()