import pygame
import random
import math
import game_consts
from game_consts import *
import sys
import Screen
import game_field
import soldier



def main():
    dungeon = game_field.generate_random_dungeon(GRID_ROWS, GRID_COLS)
    state = {'state' : game_consts.RUNNING_STATE}
    player_r, player_c = 1, 1
    font = pygame.font.SysFont("Arial", 20)
    while state['state'] == game_consts.RUNNING_STATE:
        game_screen.fill(COLOR_PANEL)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state['state'] = game_consts.LOST_STATE

            if event.type == pygame.KEYDOWN:
                dr, dc = 0, 0
                if event.key == pygame.K_UP:
                    dr = -1
                elif event.key == pygame.K_DOWN:
                    dr = 1
                elif event.key == pygame.K_LEFT:
                    dc = -1
                elif event.key == pygame.K_RIGHT:
                    dc = 1
                elif event.key == pygame.K_SPACE:
                    Screen.draw_grid_lines(dungeon)


                if dr != 0 or dc != 0:
                    player_r, player_c, new_state = soldier.move_player(dungeon, player_r, player_c, dr, dc)
                    state['state'] = new_state
                    if state['state'] == game_consts.LOST_STATE:
                        print("you are dead sonion")

        if state['state'] == game_consts.WIN_STATE:
            dungeon = game_field.generate_random_dungeon(GRID_ROWS, GRID_COLS)
            player_r, player_c = 1, 1

        # draw mines
        Screen.draw_mines(dungeon)
        # draw flag
        Screen.draw_flag()


        # draw player
        Screen.draw_player(player_c, player_r)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
