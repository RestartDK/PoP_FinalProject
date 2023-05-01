from entities import Entities
from game import Game
from entities import Entities
import pygame

# Goal of game: Go through labyrinth with 5 rooms and try to pick up many items as possible.
# Each item will have a rarity, each rarity will correspond to a number of points. There are
# traps and chests along the way to either improve chance of picking up good item or dying
# before the finish line. You can fuse 2 items to get one with higher rarity and get more points.
# Character will have 3 lives each trap will take off 1 life. Will allow player to fuse 2 items 
# with the same rarity. If you get 3 legendaries, automatically end the run you have won.
# Chests will only have epic or legendary items

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROOM_WIDTH = 400
ROOM_HEIGHT = 400

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