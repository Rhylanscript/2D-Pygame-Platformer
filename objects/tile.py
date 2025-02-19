# external imports
import pygame

# tile class
class Tile(pygame.Rect):
    # constructor
    def __init__(self, x:int, y:int, size:int) -> None:
        super().__init__(x, y, size, size)
    
    # draw method
    def draw(self, screen:pygame.Surface, ox:int, sox:int, soy:int) -> None:
        pygame.draw.rect(screen, (128, 128, 128), (self.x - ox + sox, self.y + soy, self.width, self.height))