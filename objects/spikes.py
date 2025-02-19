# external imports
import pygame

# spike class
class Spike(pygame.Rect):
    # constructor
    def __init__(self, x:int, y:int, size:int, direction:str):
        # call the super constructor based on the direction
        super().__init__(x, y, size, size)
        self.direction = direction
        self.update_hitbox()

    def update_hitbox(self) -> None:
        if self.direction == 'up':
            self.hitbox = pygame.Rect(self.x + self.width * 0.25, self.y + self.height * 0.25, self.width * 0.5, self.height * 0.5)
        elif self.direction == 'down':
            self.hitbox = pygame.Rect(self.x + self.width * 0.25, self.y + self.height * 0.25, self.width * 0.5, self.height * 0.5)
        pass

    # draw the spike (up or down)
    def draw(self, screen:pygame.display, offset_x:int, shake_offset_x:int, shake_offset_y:int):
        self.update_hitbox()
        # store 3 points and draw a polygon based on the direction
        if self.direction == 'up':
            spike_points = [
                (self.x - offset_x + self.width // 2 + shake_offset_x, self.y + shake_offset_y),  # Top middle
                (self.x - offset_x + shake_offset_x, self.y + self.height + shake_offset_y),  # Bottom left
                (self.x - offset_x + self.width + shake_offset_x - 1, self.y + self.height + shake_offset_y)  # Bottom right
            ]
        elif self.direction == 'down':
            spike_points = [
                (self.x - offset_x + self.width // 2 + shake_offset_x, self.y + self.height + shake_offset_y),  # Bottom middle
                (self.x - offset_x + shake_offset_x, self.y + shake_offset_y),  # Top left
                (self.x - offset_x + self.width + shake_offset_x - 1, self.y + shake_offset_y)  # Top right
            ]
        # draw polygon
        pygame.draw.polygon(screen, (128, 128, 128), spike_points)
        #pygame.draw.rect(screen, (255, 0, 0), (self.hitbox.x - offset_x + shake_offset_x, self.hitbox.y + shake_offset_y, self.hitbox.width, self.hitbox.height), 1)