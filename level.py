# import external modules
import pygame, random

# import local modules
from objects.util.settings import *
from objects.util.map import LEVEL

from objects.tile import Tile
from objects.box import Box
from objects.spikes import Spike
from objects.buttons import PressButton, HoldButton
from objects.doors import PressDoor, HoldDoor

from player import Player

# main class
class Level:
    # constructor
    def __init__(self) -> None:
        # get lists and tuples from self method
        self.tiles, self.upspikes, self.dnspikes, self.boxes, self.player_start, self.press_buttons, self.hold_buttons, self.press_doors, self.hold_doors = self.load_level()
        self.spikes = self.upspikes + self.dnspikes
        self.doors = self.press_doors + self.hold_doors

        # setup player
        self.player = Player(self.player_start[0], self.player_start[1], self.tiles, self.boxes, self)
        self.player.player_start = self.player_start
        
        # world scroll x
        self.offset_x = 0

        # Screen shake variables
        self.shake_intensity = 0
        self.shake_duration = 0
        self.shake_offset_x = 0
        self.shake_offset_y = 0

    # method returns lists and tuples
    def load_level(self) -> tuple[tuple]:

        # create temp lists and tuples
        tiles = []
        up_spikes = []
        dn_spikes = []
        press_buttons = []
        hold_buttons = []
        press_doors = []
        hold_doors = []
        crates = []
        player_start = (0, 0)

        # loop through level
        for y, row in enumerate(LEVEL):
            for x, space in enumerate(row):

                # check char and if corresponding value, add to list or set tuple
                if space == 'X':    # tiles
                    tiles.append(Tile(x * SIZE, y * SIZE, SIZE))
                elif space == 'P':  # player starting pos
                    player_start = (x * SIZE + ((SIZE - PLAYER_WIDTH) // 2), y * SIZE + ((SIZE - PLAYER_HEIGHT) // 2))
                elif space == 'A':  # spikes
                    up_spikes.append(Spike(x * SIZE, y * SIZE, SIZE, 'up'))
                elif space == 'V':
                    dn_spikes.append(Spike(x * SIZE, y * SIZE, SIZE, 'down'))
                elif space == 'B':
                    crates.append(Box(x * SIZE, y * SIZE, SIZE))
                elif space == 'T':
                    press_buttons.append(PressButton(x * SIZE, y * SIZE + ((SIZE / 3) * 2), SIZE, SIZE / 3, door_id=1))  # Example door_id
                elif space == 'H':
                    hold_buttons.append(HoldButton(x * SIZE, y * SIZE + ((SIZE / 4) * 3), SIZE, SIZE / 4, door_id=1))  # Example door_id
                elif space == 'O':
                    press_doors.append(PressDoor(x * SIZE, y * SIZE, SIZE, SIZE, door_id=1))  # Example door_id
                elif space == 'D':
                    hold_doors.append(HoldDoor(x * SIZE, y * SIZE, SIZE, SIZE, door_id=1))  # Example door_id
        
        # return values
        return tiles, up_spikes, dn_spikes, crates, player_start, press_buttons, hold_buttons, press_doors, hold_doors
    
    # Function to trigger screen shake
    def trigger_shake(self, intensity:int, duration:int) -> None:
        # set values
        self.shake_intensity = intensity
        self.shake_duration = duration

    # update technical elements
    def update(self) -> None:
         # Handle screen shake effect
        if self.shake_duration > 0:
            self.shake_offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_duration -= 1
        else:
            self.shake_offset_x = 0
            self.shake_offset_y = 0

        # add boxes and tiles to player collisions
        self.player.collidable_objects = []
        self.player.collidable_objects = self.tiles + self.boxes

        # add doors to player collisions if door is active
        for door in self.doors:
            if door.active:
                self.player.collidable_objects.append(door)

        # call player update
        self.player.update()

        # Update doors
        for door in self.doors:
            door.update(self.press_buttons + self.hold_buttons)

        # Check for spike collision
        for spike in self.spikes:
            if self.player.rect.colliderect(spike.hitbox):
                self.player.reset()
                self.trigger_shake(5, 15)  # Strong shake when hitting spikes

        if self.player.dead:
            self.trigger_shake(5, 15)

        # Check for press button collision
        for btn in self.press_buttons:
            if self.player.rect.colliderect(btn) or any(box.colliderect(btn) for box in self.boxes):
                btn.pressed = True

        # Check for hold button collision
        for btn in self.hold_buttons:
            if self.player.rect.colliderect(btn) or any(box.colliderect(btn) for box in self.boxes):
                btn.held = True
            else:
                btn.held = False

        # update x offset (world scroll)
        self.offset_x = max(0, min(self.player.rect.x - WIDTH // 2, level_width - WIDTH))
    
    # draw the level
    def draw(self, screen:pygame.display, hitboxes:bool) -> None:
        # call update method
        self.update()

        # Draw tiles with shake effect
        for tile in self.tiles:
            tile.draw(screen, self.offset_x, self.shake_offset_x, self.shake_offset_y)
            
        for box in self.boxes:
            box.draw(screen, self.offset_x, self.shake_offset_x, self.shake_offset_y)
            
        # Draw spikes with shake effect
        for spike in self.upspikes:
            spike.draw(screen, self.offset_x, self.shake_offset_x, self.shake_offset_y)

        for spike in self.dnspikes:
            spike.draw(screen, self.offset_x, self.shake_offset_x, self.shake_offset_y)

        for btn in self.press_buttons:
            btn.draw(screen, self.offset_x, self.shake_offset_x, self.shake_offset_y)

        for btn in self.hold_buttons:
            btn.draw(screen, self.offset_x, self.shake_offset_x, self.shake_offset_y)

        for door in self.doors:
            door.draw(screen, self.offset_x, self.shake_offset_x, self.shake_offset_y)

        # Draw player start with shake effect
        pygame.draw.rect(screen, (50, 255, 50), (
                self.player.player_start[0] - ((SIZE - PLAYER_WIDTH) // 2) + SIZE // 4 - self.offset_x,
                self.player.player_start[1] - ((SIZE - PLAYER_HEIGHT) // 2) + SIZE // 4,
                SIZE // 2,
                SIZE // 2
            )
        )

        # Draw player with shake effect
        self.player.draw(self.offset_x + self.shake_offset_x, screen)

        # Show hitboxes if enabled
        if hitboxes:
            pygame.draw.rect(screen, (255, 0, 0), 
                                (spike.hitbox.x - self.offset_x, spike.hitbox.y, spike.hitbox.width, spike.hitbox.height), 3)
            for tile in self.tiles:
                pygame.draw.rect(screen, (0, 0, 255), 
                                (tile.x - self.offset_x, tile.y, SIZE, SIZE), 2)
            pygame.draw.rect(screen, (0, 255, 120), 
                            (self.player.rect.left - self.offset_x, self.player.rect.top, PLAYER_WIDTH, PLAYER_HEIGHT), 3)