# game.py
# In this file the GUI of the game will be defined here

import pygame, sys
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
        
    def check_collisions(self, keys_pressed, chest_sprites, item_sprites, trap_sprites):
        collided_chests = pygame.sprite.spritecollide(self, chest_sprites, False)
        collided_items = pygame.sprite.spritecollide(self, item_sprites, False)
        collided_traps = pygame.sprite.spritecollide(self, trap_sprites, False)
        
        if len(collided_chests) > 0:
            # The character has collided with a chest
            # Call the openChest() method to interact with the chest
            for front_end_chest in collided_chests:
                chest = front_end_chest.entity
                self.openChest(chest)
                front_end_chest.kill()
            
            
        if len(collided_items) > 0:
            # The character has collided with an item
            # Call the pickUpItem() method to interact with the item
            for front_end_item in collided_items:
                item = front_end_item.entity
                self.pickUpItem(item)
                front_end_item.kill()
            
            
        if len(collided_traps) > 0:
            # The character has collided with a trap
            # Call the stepTrap() method to interact with the trap
            for front_end_trap in collided_traps:
                trap = front_end_trap.entity
                collided_traps.remove(front_end_trap)
                self.stepTrap(trap)
        
    def openChest(self, chest: Chest):
        item = chest.getItem()
        if item != None:
                self.character.addItem(item)
                # Updating score with new item
                self.character.changeScore()
                
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print("You just picked up: ", chest.getItem().getName(), " (", chest.getItem().getName(), ")")
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
        
    def update(self):
        pass
    
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

# TODO: Keep this here and move other methods to a frontend.py file
# Controller class to connect the frontend and backend
class Game():
    def __init__(self, labyrinth, SCREEN_WIDTH: int, SCREEN_HEIGHT: int):
        pygame.init()
        self.labyrinth = labyrinth
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
        self.chest_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.trap_sprites = pygame.sprite.Group()
        
    def handle_events(self):
        self.game_state.stateManager()
            
    def intro_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type ==  pygame.MOUSEBUTTONDOWN:
                self.game_state.state = "mainGame"
    
    def mainGame_events(self):
        self.initialiseEntities(labyrinth[self.room_count])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        

    def changeRoom_events(self):
        if self.room_count > len(labyrinth):
            self.game_state.state = "end"
            
        self.room_count += 1
    
    def end_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
    def update(self, dt):
        keys_pressed = pygame.key.get_pressed()
        self.backend_character.update(keys_pressed, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.frontend_character.update()
        self.frontend_character.check_collisions(keys_pressed, self.chest_sprites, self.item_sprites, self.trap_sprites)
        
    def drawRoom(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.frontend_character.image, self.frontend_character.rect)
        self.chest_sprites.draw(self.screen)
        self.item_sprites.draw(self.screen)
        self.trap_sprites.draw(self.screen)
        pygame.display.flip()
    
    def drawIntro(self):
        self.screen.fill((255, 255, 255))
        # Draw the background and start screen
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.start_button, (SCREEN_HEIGHT/2 - 130, SCREEN_WIDTH/2 - 200)) 
        pygame.display.flip()
    
    def initialiseEntities(self, room):
        self.chest_sprites.empty()
        self.item_sprites.empty()
        self.trap_sprites.empty()
        self.createFrontEndItems(room)
        self.createFrontEndChests(room)
        self.createFrontEndTraps(room)
    
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
            frontend_trap = FrontEndEntity("assets/traps/trap.png", trap)
            self.trap_sprites.add(frontend_trap)

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
        dt = clock.tick(60) / 1000.0
        game.update(dt)
        
        # Draw the screen
        game.drawRoom()
        
    def changeRoom(self):
        # Handle changing room events
        game.changeRoom_events()
        
    def end(self):
        # Handle end game events
        game.end_events()
        
        # Update game state
        dt = clock.tick(60) / 1000.0
        game.update(dt)
        
        # Draw the screen
        game.drawRoom()
        
    def stateManager(self):
        if self.state == "intro":
            self.intro()
        if self.state == "mainGame":
            self.mainGame() 
        if self.state == "changeRoom":
            self.changeRoom()
        if self.state == "end":
            self.end()
            
# TODO: Put this in run method
if __name__ == "__main__":
    #Initalise Game Object (controller)
    entities = Entities(5, ROOM_WIDTH, ROOM_HEIGHT)
    labyrinth = entities.createLabyrinth()
    
    for room in labyrinth:
        print(room.getChests())
        
    game = Game(labyrinth, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        # Handle events
        game.handle_events()