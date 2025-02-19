# external imports
import pygame

# Box class
class Box(pygame.Rect):
    # constructor
    def __init__(self, x:int, y:int, size:int) -> None:
        super().__init__(x, y, size, size)

    # draw method (draws outline and filled rectangle)
    def draw(self, screen:pygame.display, ox:int, sox:int, soy:int) -> None:
        pygame.draw.rect(screen, (180, 100, 30),
                         (self.x - ox + sox, self.y - soy, self.width, self.height))
        pygame.draw.rect(screen, (160, 85, 20),
                         (self.x - ox + sox, self.y - soy, self.width, self.height), 3)