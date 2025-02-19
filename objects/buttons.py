# external imports
import pygame, random

# local imports
from objects.util.settings import *
from objects.util.map import LEVEL
from player import Player

# pressbutton class
class PressButton(pygame.Rect):
    # constructor
    def __init__(self, x:int, y:int, width:int, height:int, door_id:int) -> None:
        # call the super constructor
        super().__init__(x, y, width, height)
        self.pressed = False
        self.door_id = door_id

    # draw the button
    def draw(self, screen:pygame.display, offset_x:int, shake_offset_x:int, shake_offset_y:int) -> None:
        color = (255, 0, 0) if self.pressed else (128, 0, 0)  # Red when pressed, dark red otherwise
        pygame.draw.rect(screen, color, (self.x - offset_x + shake_offset_x, self.y + shake_offset_y, self.width, self.height+1))

# holdbutton class
class HoldButton(pygame.Rect):
    # constructor
    def __init__(self, x:int, y:int, width:int, height:int, door_id:int) -> None:
        # call the super constructor
        super().__init__(x, y, width, height)
        self.held = False
        self.door_id = door_id

    # draw the button
    def draw(self, screen:pygame.display, offset_x:int, shake_offset_x:int, shake_offset_y:int) -> None:
        color = (0, 0, 255) if self.held else (0, 0, 128)  # Blue when held, dark blue otherwise
        pygame.draw.rect(screen, color, (self.x - offset_x + shake_offset_x, self.y + shake_offset_y, self.width, self.height))