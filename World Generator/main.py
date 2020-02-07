import pygame
import math
import csv

from menu import *
from world import *

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
game = 0
game_world = None


mouse_pos = (0, 0)
delta_mouse_pos = (0, 0)

menu_top_level = main_menu(screen)

def main():
    pygame.display.set_caption("Little World Generator")
    


if __name__ == "__main__":
    main()

def start_game():
    global game
    global game_world
    game = 1

    game_world = world(screen, (50, 50 ), 1)

def mouse_pos_change(pos):
    global mouse_pos
    delta_mouse_pos = (0, 0)

    if mouse_pos != (0, 0):
        delta_mouse_pos = (pos[0] - mouse_pos[0], pos[1] - mouse_pos[1])

    mouse_pos = pos

    return delta_mouse_pos

def release_mouse():
    global mouse_pos
    mouse_pos = (0, 0)
    



mainloop = True
update_tiles_counter = 0

while mainloop:
    update_tiles_counter += 1

    mouse_pos_cur = pygame.mouse.get_pos()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False

        if pygame.mouse.get_pressed()[0] and game_world:
            game_world.move_world(mouse_pos_change(mouse_pos_cur))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                game_world.zoom_world(-1)
            if event.button == 5:
                game_world.zoom_world(1)

        if event.type == pygame.MOUSEBUTTONUP:
            release_mouse()


    


    if not game:
        screen.fill(COLOR_BLACK)
        game_state = main_menu.display(menu_top_level)
        
        if game_state == 1:
            screen.fill(COLOR_BLACK)
            pygame.display.flip()

            start_game()
        elif game_state == 0:
            mainloop = False

    elif game and update_tiles_counter >= 2:
        screen.fill(COLOR_BLACK)
        print(game_world.is_over_tile(mouse_pos_cur))

        for tile in game_world.get_tile_list():
            game_tile.display(tile)

        
        update_tiles_counter = 0

    

    pygame.display.flip()


    

