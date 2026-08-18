import pygame
import game_consts
from game_consts import *
from main import *
import teleport



def move_player(grid, player_r, player_c, dr, dc):
    new_r = player_r + dr
    new_c = player_c + dc
    new_state = game_consts.RUNNING_STATE
   # new_state_teleport = game_consts.RUNNING_STATE
    # check every cell covered by the new 6x2 footprint
    for pr in range(game_consts.PLAYER_ROWS):
        for pc in range(game_consts.PLAYER_COLS):
            check_r = new_r + pr
            check_c = new_c + pc
            grid_len = len(grid)
            grid_0_len = len(grid[0])
            # out of bounds check or hitting a wall
            if check_r >= len(grid) or check_c >= len(grid[0])-1:
                return player_r, player_c, new_state
            if check_r < 0 or check_c < 0:
                return player_r, player_c, new_state

    # process items within the new footprint space
    for pr in range(game_consts.PLAYER_ROWS):
        for pc in range(game_consts.PLAYER_COLS):
            target_r = new_r + pr
            target_c = new_c + pc

            if grid[target_r][target_c] == game_consts.TILE_DIAMOND:
                new_state = game_consts.state['state'] = game_consts.WIN_STATE
            elif grid[new_r + 3][target_c] == game_consts.TILE_MINE:
                new_state = game_consts.LOST_STATE
                #  ברגע שנגעתי בטלפורת
            elif grid[target_r][target_c+1] == game_consts.TILE_PIT:
                new_state = game_consts.TELEPORT_STATE




    return new_r, new_c, new_state