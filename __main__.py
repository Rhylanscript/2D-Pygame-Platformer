# external imports
import pygame

# local imports
from objects.util.settings import *
from level import Level

# setup pygame objects
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# mainloop util
level = Level()
running = True
show_hitboxes = False

# mainloop
while running:
    # clear screen
    screen.fill((0, 0, 0))

    # event handling
    for event in pygame.event.get():

        # on quit
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

        # on keydown
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level.player.jump_pressed = True

            if event.key == pygame.K_DOWN:
                level.player.down_pressed = True

            # press r to reset the level
            if event.key == pygame.K_r:
                level.player.reset()
                level.trigger_shake(3, 10)  # Shake when resetting

            # press c to show hitboxes
            if event.key == pygame.K_c:
                show_hitboxes = not show_hitboxes

        # on keyup
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                level.player.jump_pressed = False

            if event.key == pygame.K_DOWN:
                level.player.down_pressed = False

    # draw the game
    level.draw(screen, show_hitboxes)

    # update window
    pygame.display.flip()
    clock.tick(FPS)

# post process
pygame.quit()