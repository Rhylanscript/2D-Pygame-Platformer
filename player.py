# external imports
import pygame

# local imports
from objects.util.settings import *

# Player Class
class Player:
    # constructor
    def __init__(self, x:int, y:int, tiles:list, boxes:list, level) -> None:
        self.level = level

        # setup rect (hitbox)
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.height = PLAYER_HEIGHT
        self.width = PLAYER_WIDTH

        # lists and tiles needed for collisions and game logic
        self.tiles = tiles
        self.boxes = boxes
        #self.doors = doors
        self.box_start_positions = [(box.x, box.y) for box in self.boxes]
        self.collidable_objects = self.tiles + self.boxes #+ self.doors
        self.player_start = (0, 0)

        self.box_x_velocities = [0] * len(self.boxes)
        self.box_y_velocities = [0] * len(self.boxes)

        # player x and y velocity
        self.xv = 0
        self.yv = 0

        # flag bools
        self.on_ground = False
        self.jump_pressed = False
        self.down_pressed = False
        self.left_down = False
        self.right_down = False

        self.sliding = False
        self.dead = False
        self.carrying_box = False

        self.dashing = False
        self.has_dashed = False

        # track player jumps
        self.jumps = 0

        # dash variables
        self.dash_speed = 20
        self.dash_time = 10         # frames
        self.dash_cooldown = 30     # frames before dash can be used again
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.dash_direction = 0

    def box_above(self) -> bool:
        for box in self.boxes:
            if self.rect.colliderect(pygame.Rect(box.x, box.y + SIZE, SIZE, SIZE)):
                return True
        return False

    # move the player along x and y axis, check collisions
    def move(self, dx:int, dy:int) -> None:
        # check if player dashing
        if not self.dashing:
            # Horizontal Movement
            self.rect.x += dx
            touching_wall = False

            push_force = 0.5
            friction = 0.1
            max_speed = 3
            
            for i, box in enumerate(self.boxes):
                if self.rect.colliderect(box):
                    if self.down_pressed and self.on_ground:
                        ogv = self.box_x_velocities[i]
                        if self.right_down and self.rect.right >= box.left:
                            self.box_x_velocities[i] += push_force
                        elif self.left_down and self.rect.left <= box.right:
                            self.box_x_velocities[i] -= push_force

                        # handling max velocity
                        self.box_x_velocities[i] = max(-max_speed, min(max_speed, self.box_x_velocities[i]))
                        collide = False
                        if abs(self.box_x_velocities[i]) > 0.05:
                            new_x = box.x + self.box_x_velocities[i]
                            if any(obj.colliderect(pygame.Rect(new_x, box.y, SIZE, SIZE)) for obj in self.collidable_objects if obj != box):
                                self.box_x_velocities[i] = 0
                                collide = True
                            

                        # move stacked boxes
                        for j, other_box in enumerate(self.boxes):
                            if i != j and other_box.colliderect(pygame.Rect(box.x, box.y - SIZE, SIZE, SIZE)):
                                if collide:
                                    self.box_x_velocities[j] = ogv
                                else:
                                    self.box_x_velocities[j] = self.box_x_velocities[i]

            # apply velocity and friction
            for i, box in enumerate(self.boxes):
                if abs(self.box_x_velocities[i]) > 0.05:
                    new_x = box.x + self.box_x_velocities[i]

                    # check for collisions before moving boxes
                    if not any(obj.colliderect(pygame.Rect(new_x, box.y, SIZE, SIZE)) for obj in self.collidable_objects if obj != box):
                        box.x = new_x
                    else:
                        self.box_x_velocities[i] = 0

                    # apply friction
                    self.box_x_velocities[i] *= (1 - friction)
                else:
                    self.box_x_velocities[i] = 0
            
            # loop through tiles
            for obj in self.collidable_objects:
                # check player collision with targeted tile
                if self.rect.colliderect(obj): #and (not isinstance(obj, Door) or obj.active):
                    # place player next to wall if inside
                    if dx > 0:
                        self.rect.right = obj.left
                        touching_wall = True
                        # check sliding
                        if self.right_down and not self.on_ground and self.yv > 0:
                            self.sliding = True
                    elif dx < 0:
                        self.rect.left = obj.right
                        touching_wall = True
                        # check sliding
                        if self.left_down and not self.on_ground and self.yv > 0:
                            self.sliding = True

            # Reset sliding if no wall is being touched
            if not touching_wall:
                self.sliding = False

            # Reset slide if on ground
            if self.on_ground:
                self.sliding = False

            # Vertical Movement
            if not self.sliding:
                # change player y
                self.rect.y += dy
            else:
                # if sliding, make player fall slower
                if not self.on_ground and self.sliding:
                    self.rect.y += SLIDE_SPEED
                    self.yv = SLIDE_SPEED

            # check vertical collisions (jumps into ceil, falls on ground)
            self.on_ground = False
            for obj in self.collidable_objects:
                if self.rect.colliderect(obj): #and (not isinstance(obj) or obj.active):
                    if dy > 0:
                        self.rect.bottom = obj.top
                        # update player on ground
                        self.on_ground = True
                        self.yv = 0
                    elif dy < 0:
                        self.rect.top = obj.bottom
                        self.yv = 0

    # method to make player dash
    def dash(self) -> None:
        # check cooldown timer is 0 and make sure player hasnt dashed already since last ground touch
        if self.dash_cooldown_timer == 0 and not self.dashing and not self.has_dashed and not self.box_above():
            # dash in specified direction only if key down
            if self.left_down or self.right_down:
                self.dashing = True
                self.dash_timer = self.dash_time
                self.dash_cooldown_timer = self.dash_cooldown
                self.dash_direction = 1 if self.xv >= 0 else -1
                self.has_dashed = True
                self.width, self.height = 56, 40

    # method to update player
    def update(self) -> None:
        # get keypresses
        keys = pygame.key.get_pressed()

        # update dash cooldown
        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= 1

        # different logic for dashing
        if self.dashing:
            # yv can only decrease when dashing
            if self.yv < 0:
                self.yv += GRAVITY
                self.rect.y += self.yv
            else:
                self.yv = 0

            # apply yv
            self.rect.y += self.yv

            # check for collisions 
            for _ in range(self.dash_speed // 3):
                self.rect.x += 3 * self.dash_direction
                for obj in self.collidable_objects:
                    if self.rect.colliderect(obj) and (not isinstance(obj) or obj.active):

                        # x collisions
                        if self.dash_direction == 1:
                            self.rect.x -= 3
                        else:
                            self.rect.x += 3
                        
                        # y collisions
                        if self.yv > 0:
                            self.rect.bottom = obj.top
                        elif self.yv < 0:
                            self.rect.top = obj.bottom

                        # update flags
                        self.dashing = False

                        # break from dash
                        return

            # update dash timer
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.dashing = False
        # otherwise apply movement normally
        else:
            # apply gravity
            self.yv += GRAVITY

            # get key input
            move_left = keys[pygame.K_LEFT]
            move_right = keys[pygame.K_RIGHT]

            # Constants (should prob go in settings.py but idgaf)
            AIR_ACCELERATION = 0.3
            AIR_FRICTION = 0.3
            MAX_AIR_SPEED = PLAYER_SPEED

            # x movement
            if self.on_ground:
                # if on ground 'sticky' movement
                self.xv = (move_right - move_left) * PLAYER_SPEED
                if self.box_above():
                    self.xv *= 0.5
            else:
                # if in air 'slippery' movement (chatgpt cooked ngl)
                if move_right:
                    self.xv += AIR_ACCELERATION
                elif move_left:
                    self.xv -= AIR_ACCELERATION
                else:
                    if self.xv > 0:
                        self.xv = max(0, self.xv - AIR_FRICTION)
                    elif self.xv < 0:
                        self.xv = min(0, self.xv + AIR_FRICTION)
                self.xv = max(-MAX_AIR_SPEED, min(MAX_AIR_SPEED, self.xv))

            # jump logic
            if self.jump_pressed and not self.carrying_box and not self.box_above():
                # increment jumps
                self.jumps += 1
                if self.sliding:

                    # sliding logic
                    self.jumps = 1
                    self.yv = JUMP_STRENGTH

                    # check jump direction, apply xv
                    if self.left_down:
                        self.xv = PLAYER_SPEED
                    elif self.right_down:
                        self.xv = -PLAYER_SPEED

                    # stop sliding after jump
                    self.sliding = False 
                else:
                    # otherwise, check if player hasnt used up double jump
                    if self.jumps < 2:
                        self.yv = JUMP_STRENGTH

                # update flag
                self.jump_pressed = False

            # Update movement keys state
            self.left_down = keys[pygame.K_LEFT]
            self.right_down = keys[pygame.K_RIGHT]

            # Reset sliding if no wall is being touched
            if not self.left_down and not self.right_down:
                self.sliding = False

            # reset jumps if on ground
            if self.on_ground:
                self.jumps = 0

            # move player
            self.move(self.xv, self.yv)

            # Handle pushing boxes
            if self.down_pressed:
                for box in self.boxes:
                    if self.rect.colliderect(box):
                        if self.left_down:
                            box.x_velocity = -PLAYER_SPEED
                        elif self.right_down:
                            box.x_velocity = PLAYER_SPEED

        # Dash activation
        if keys[pygame.K_SPACE]:
            self.dash()

        # Reset dash once ground reached
        if self.on_ground:
            self.has_dashed = False

        # Respawn if falling
        if self.rect.top > HEIGHT:
            self.dead = True
            self.reset()
        else:
            self.dead = False

        # reset player size
        if not self.dashing:
            self.width, self.height = PLAYER_WIDTH, PLAYER_HEIGHT

        BOX_GRAVITY = 0.5
        BOX_MAX_FALL_SPEED = 30

        for i, box in enumerate(self.boxes):
            self.box_y_velocities[i] += BOX_GRAVITY
            self.box_y_velocities[i] = min(self.box_y_velocities[i], BOX_MAX_FALL_SPEED)

            new_y = box.y + self.box_y_velocities[i] + 1
            box_rect = pygame.Rect(box.x, new_y, SIZE, SIZE)
    
            # check for collisions with tiles and other boxes
            colliding = any(obj.colliderect(box_rect) for obj in self.collidable_objects if obj != box)

            if self.box_above() and self.yv == 0 and self.rect.colliderect(box_rect):
                self.box_y_velocities[i] = 0
                box.bottom = self.rect.top
                self.carrying_box = True
            elif not colliding:
                box.y = new_y
                self.carrying_box = False
            else:
                self.box_y_velocities[i] = 0
                self.carrying_box = False

            # move any satcked boxes
            for j, other_box in enumerate(self.boxes):
                if i != j and other_box.colliderect(pygame.Rect(box.x, box.y - SIZE, SIZE, SIZE)):
                    self.box_y_velocities[j] = self.box_y_velocities[i]

    # method to reset player and flags
    def reset(self) -> None:
        self.rect.topleft = self.player_start
        self.sliding = False
        self.dashing = False
        self.has_dashed = True
        self.left_down = False
        self.right_down = False
        self.on_ground = False
        self.yv = 0
        self.xv = 0
        self.jumps = 5

        # reset boxes
        for i, box in enumerate(self.boxes):
            box.topleft = self.box_start_positions[i]

        # reset box velocities
        self.box_x_velocities = [0] * len(self.boxes)
        self.box_y_velocities = [0] * len(self.boxes)

        for btn in self.level.press_buttons:
            btn.pressed = False

    # draw the player
    def draw(self, offset_x:int, surface: pygame.Surface) -> None:
        # Set player color (yellow if dashing)
        colour = (255, 255, 0) if self.dashing else (255, 255, 255)
        
        # Find the center point of the player
        center_x = self.rect.centerx - offset_x
        center_y = self.rect.centery

        # Calculate the top-left position based on the current width and height
        draw_x = center_x - self.width // 2
        draw_y = center_y - self.height // 2

        # Draw player rect centered at the same point
        pygame.draw.rect(surface, colour, (draw_x, draw_y, self.width, self.height))