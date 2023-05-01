# game.py
# This file contains the controller class of the application

import pygame, sys
from character import Character
from room import Room
from entities import Entities
from frontend import FrontEndCharacter, FrontEndGameover, FrontEndEntity, FrontEndExit

# Controller class to connect the frontend and backend
class Game():
    def __init__(self, entities: Entities, SCREEN_WIDTH: int, SCREEN_HEIGHT: int):
        pygame.init()
        self.entities = entities
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.labyrinth = self.entities.createLabyrinth()
        self.game_state = GameState(self)
        self.room_count = 0
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        self.gameover_screen = FrontEndGameover("assets/buttons/gameover.png", "assets/buttons/replay.png", self.backend_character.getScore(), self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.secretEnd_screen = FrontEndGameover("assets/buttons/crown.png", "assets/buttons/replay.png", self.backend_character.getScore(), self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.room_change = False
        
        self.font = pygame.font.SysFont("monospace", 24)
        self.hud = self.font.render("Score: " + str(self.backend_character.getScore()) + " Health: " + 
                                    str(self.backend_character.getHealth()), 1, (255, 255, 255)) 
        
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
                elif event.key == pygame.K_RETURN:
                    self.labyrinth = self.entities.createLabyrinth()
                    self.game_state.state = "changeRoom"
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.labyrinth = self.entities.createLabyrinth()
                self.game_state.state = "changeRoom"
    
    def mainGame_events(self):
        # Updates the score label on the gameoverscreen
        self.gameover_screen.updateScoreLabel(self.backend_character.getScore())
        self.secretEnd_screen.updateScoreLabel(self.backend_character.getScore())
        self.hud = self.font.render("Score: " + str(self.backend_character.getScore()) + " Health: " + 
                                    str(self.backend_character.getHealth()), 1, (255, 255, 255))
        
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
        
        # If the character collides with any exit or trap, run appropriate method
        self.frontend_character.mandatoryCollisions(self.trap_sprites, self.exit_sprites, self.game_state, self)
        
        # If the character collides with the exit, change room and make room change false to continue labyrinth
        if not pygame.sprite.spritecollide(self.frontend_character, self.exit_sprites, False):
            self.room_change = False

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
        self.backend_character.update(keys_pressed, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.frontend_character.update()
        
    def drawRoom(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.frontend_character.image, self.frontend_character.rect)
        self.chest_sprites.draw(self.screen)
        self.item_sprites.draw(self.screen)
        self.trap_sprites.draw(self.screen)
        self.exit_sprites.draw(self.screen)
        self.screen.blit(self.hud, (500, 10))
        pygame.display.flip()
    
    def drawIntro(self):
        self.screen.fill((255, 255, 255))
        # Draw the background and start screen
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.start_button, (self.SCREEN_HEIGHT/2 - 130, self.SCREEN_WIDTH/2 - 200)) 
        pygame.display.flip()
        
    def drawEnd(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.gameover_screen.image, self.gameover_screen.rect)
        self.screen.blit(self.gameover_screen.score_label, (self.SCREEN_WIDTH/2 - 150, self.SCREEN_HEIGHT/2))
        self.screen.blit(self.gameover_screen.replay_button, self.gameover_screen.replay_button_rect)
        pygame.display.flip()
    
    def drawSecretEnd(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.secretEnd_screen.image, self.secretEnd_screen.rect)
        self.screen.blit(self.secretEnd_screen.score_label, (self.SCREEN_WIDTH/2 - 150, self.SCREEN_HEIGHT/2))
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
        self.game.intro_events()
        
        # Draw everything
        self.game.drawIntro()

    def mainGame(self):
        # Handle room events
        self.game.mainGame_events()
        
        # Update game state
        self.game.update()
        
        # Draw the screen
        self.game.drawRoom()
        
    def changeRoom(self):
        # Handle changing room events
        self.game.changeRoom_events()
        
    def end(self):
        # Handle end game events
        self.game.end_events()
        
        # Draw the screen
        self.game.drawEnd()
        
    def secretEnd(self):
        # Handle secret end game events
        self.game.secretEnd_events()
        
        # Draw the screen
        self.game.drawSecretEnd()
        
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