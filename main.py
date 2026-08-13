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
    start_bool = True
    dungeon = game_field.generate_random_dungeon_grass(GRID_ROWS, GRID_COLS)
    dungeon_mines = game_field.generate_random_dungeon_mines(GRID_ROWS, GRID_COLS)
    state = {'state' : game_consts.RUNNING_STATE}
    player_r, player_c = 1, 1
    while state['state'] == game_consts.RUNNING_STATE:
        game_screen.fill(COLOR_PANEL)
        # draw grass
        Screen.draw_grass(dungeon)
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
                elif event.key == pygame.K_RETURN:
                    game_screen.fill(COLOR_PANEL)
                    Screen.draw_grid_lines(dungeon)
                    Screen.draw_mines(dungeon_mines)
                    Screen.draw_night_player(player_c, player_r)
                    pygame.display.flip()
                    pygame.time.wait(1000)


                if dr != 0 or dc != 0:
                    player_r, player_c, new_state = soldier.move_player(dungeon_mines, player_r, player_c, dr, dc)
                    state['state'] = new_state
                    if state['state'] == game_consts.LOST_STATE:
                        game_screen.fill((0, 0, 0))
                        Screen.draw_lose_message()
                        pygame.display.flip()
                        pygame.time.wait(3000)

        if state['state'] == game_consts.WIN_STATE:
            game_screen.fill((0,0,0))
            Screen.draw_win_message()
            pygame.display.flip()
            pygame.time.wait(3000)

        # draw flag
        Screen.draw_flag()

        # draw player
        Screen.draw_player(player_c, player_r)
        pygame.display.flip()
        if start_bool:
            Screen.draw_welcome_message()
            pygame.display.flip()
            pygame.time.wait(3000)
            start_bool = False
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
