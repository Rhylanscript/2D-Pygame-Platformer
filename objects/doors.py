# external imports
import pygame

# local imports
from objects.buttons import PressButton, HoldButton

# door object
class Door(pygame.Rect):
    # constructor
    def __init__(self, x:int, y:int, width:int, height:int, door_id:int) -> None:
        super().__init__(x, y, width, height)
        self.door_id = door_id  # id
        self.active = True      # is enabled?

    # make sure method is added (overwritten)
    def update(self, buttons:list) -> None:
        raise NotImplementedError("This method should be overridden by subclasses")

    # draw door
    def draw(self, screen:pygame.display, offset_x:int, shake_offset_x:int, shake_offset_y:int) -> None:
        if self.active:
            pygame.draw.rect(screen, self.color, (self.x - offset_x + shake_offset_x, self.y + shake_offset_y, self.width, self.height))

    # draw door hitbox
    def draw_hitbox(self, screen:pygame.display, offset_x:int, shake_offset_x:int, shake_offset_y:int) -> None:
        if self.active:
            pygame.draw.rect(screen, (255, 0, 0), (self.x - offset_x + shake_offset_x, self.y + shake_offset_y, self.width, self.height), 1)

# inherit from door
class PressDoor(Door):
    def __init__(self, x:int, y:int, width:int, height:int, door_id:int) -> None:
        super().__init__(x, y, width, height, door_id)
        self.color = (255, 0, 0)  # Red

    # overwrite method
    def update(self, buttons:list) -> None:
        for button in buttons:
            if isinstance(button, PressButton) and button.pressed and button.door_id == self.door_id:
                self.active = False
                return
        self.active = True

# inherit from door
class HoldDoor(Door):
    def __init__(self, x:int, y:int, width:int, height:int, door_id:int) -> None:
        super().__init__(x, y, width, height, door_id)
        self.color = (0, 0, 255)  # Blue

    def update(self, buttons:list) -> None:
        for button in buttons:
            if isinstance(button, HoldButton) and button.held and button.door_id == self.door_id:
                self.active = False
                return
        self.active = True