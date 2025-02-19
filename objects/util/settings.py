# import levels
from objects.util.map import LEVEL

# Constants
SIZE = 64
FPS = 60
GRAVITY = 0.5

# player variables
PLAYER_WIDTH, PLAYER_HEIGHT = 48, 56
#PLAYER_WIDTH, PLAYER_HEIGHT = SIZE, SIZE
JUMP_STRENGTH = -11.5
PLAYER_SPEED = 7
SLIDE_SPEED = 1

show_hitboxes = False

# Load Level
level_width = max(len(row) for row in LEVEL) * SIZE
level_height = len(LEVEL) * SIZE

# screen dimensions
WIDTH = 1200
HEIGHT = level_height