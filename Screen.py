
import pygame
import game_consts
from game_consts import *
import time

# draw grid lines
def draw_grid_lines(dungeon):
    for r in range(game_consts.GRID_ROWS):
        for c in range(game_consts.GRID_COLS):
            rect_x = c * game_consts.CELL_SIZE
            rect_y = r * game_consts.CELL_SIZE

            tile_type = dungeon[r][c]
            # color = (COLOR_PANEL)
            color = ((0, 0, 0))
            if tile_type == game_consts.TILE_EMPTY:
                color = game_consts.COLOR_EMPTY

            pygame.draw.rect(game_consts.game_screen, color, (rect_x, rect_y, game_consts.CELL_SIZE - 1, game_consts.CELL_SIZE - 1))
# draw mines
def draw_mines(dungeon):
    # draw mines
    for r in range(game_consts.GRID_ROWS):
        c = 0
        while c < game_consts.GRID_COLS:
            tile_type = dungeon[r][c]
            if tile_type == game_consts.TILE_MINE:
                rect_x = (c + 1) * game_consts.CELL_SIZE
                rect_y = r * game_consts.CELL_SIZE
                draw_image('mine', rect_x, rect_y, 3 * game_consts.CELL_SIZE, 1 * game_consts.CELL_SIZE)
                c += 3
            else:
                c += 1
# draw grass
def draw_grass(dungeon):
    # draw grass
    for r in range(game_consts.GRID_ROWS):
        c = 0
        while c < game_consts.GRID_COLS:
            tile_type = dungeon[r][c]
            if tile_type == game_consts.TILE_GRASS:
                rect_x = (c + 1) * game_consts.CELL_SIZE
                rect_y = r * game_consts.CELL_SIZE
                draw_image('grass', rect_x, rect_y, 3 * game_consts.CELL_SIZE, 2 * game_consts.CELL_SIZE)
                c += 3
            else:
                c += 1
# draw flag
def draw_flag():
    rect_x = (game_consts.GRID_COLS - 3) * game_consts.CELL_SIZE
    rect_y = (game_consts.GRID_ROWS - 3) * game_consts.CELL_SIZE
    draw_image('flag', rect_x, rect_y, 3 * game_consts.CELL_SIZE, 3 * game_consts.CELL_SIZE)
# draw player
def draw_player(player_c, player_r):
    # draw large player: scale width by PLAYER_COLS (2) and height by PLAYER_ROWS (6)
    player_x = player_c * game_consts.CELL_SIZE + 4
    player_y = player_r * game_consts.CELL_SIZE + 4
    player_width = (game_consts.CELL_SIZE * 3) - 8
    player_height = (game_consts.CELL_SIZE * 4) - 8
    # pygame.draw.rect(screen, COLOR_PLAYER, (player_x, player_y, player_width, player_height))
    draw_image('soldier', player_x, player_y, player_width, player_height)


def draw_night_player(player_c, player_r):
    # draw large player: scale width by PLAYER_COLS (2) and height by PLAYER_ROWS (6)
    player_x = player_c * game_consts.CELL_SIZE + 4
    player_y = player_r * game_consts.CELL_SIZE + 4
    player_width = (game_consts.CELL_SIZE * 3) - 8
    player_height = (game_consts.CELL_SIZE * 4) - 8
    # pygame.draw.rect(screen, COLOR_PLAYER, (player_x, player_y, player_width, player_height))
    draw_image('soldier_night', player_x, player_y, player_width, player_height)




def get_image(image_path, radius_x, radius_y):
    # load the actual image
    raw_img = pygame.image.load(image_path).convert_alpha()

    # scale the loaded image
    scaled_img = pygame.transform.smoothscale(raw_img, (radius_x, radius_y))

    # create the transparent surface
    target_surf = pygame.Surface((radius_x, radius_y), pygame.SRCALPHA)
    # pygame.SRCALPHA pixel transparency using alpha aka every pixel has its own transparency which windows ignores

    target_surf.blit(scaled_img, (0, 0) )

    return target_surf

IMAGES_LOADED = {}
def draw_image(image_name, rect_x, rect_y, size_x, size_y):
    img = f'Images/{image_name}.png'

    # only load and mask crop the image if the color is not loaded yet
    if img not in IMAGES_LOADED:
        # adding to loaded dict to not do it again. randomly thought about it since we can practically put anything in dict/list
        IMAGES_LOADED[img] = get_image(img, size_x, size_y)

    # otherwise it would overload it as like loading again and again same thing is insane for it, we just have few options, if we can cache it why not.
    avatar_circle = IMAGES_LOADED[img]

    # the positions, I could just write in like func itself but so much code I need to split this
    blit_x = rect_x
    blit_y = rect_y

    # display finally the circle on the main screen!!!
    game_consts.game_screen.blit(avatar_circle, (blit_x, blit_y))
# draw welcome
def draw_welcome_message():
    draw_message('Welcome to The Flag game.\n Have Fun!', 20,
                 (255, 255, 255), (20, 20))
# draw lose
def draw_lose_message():
    draw_message('You lost sonion', 200,
                 (255, 0, 0), (100, game_consts.HEIGHT / 2 - 200))
# draw win
def draw_win_message():
    draw_message('You won sonion', 200,
                 (255, 255, 255), (100, game_consts.HEIGHT / 2 - 200))
def draw_message(message, font_size, color, location):
    font = pygame.font.SysFont("Arial", font_size)
    text_img = font.render(message, True, color)
    game_consts.game_screen.blit(text_img, location)