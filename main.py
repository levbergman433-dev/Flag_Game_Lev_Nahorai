import pygame
import random
import math
import sys
import game_consts
from game_consts import *
import Screen
import game_field
import soldier
import database
# Buffer storage dictionary for keys 1-9
key_press_times = {}
# Keys for the corresponding figures
NUMBER_KEYS = {
    pygame.K_1: 1,
    pygame.K_2: 2,
    pygame.K_3: 3,
    pygame.K_4: 4,
    pygame.K_5: 5,
    pygame.K_6: 6,
    pygame.K_7: 7,
    pygame.K_8: 8,
    pygame.K_9: 9,
}
# לפני שהמשחק מתחיל לרוץ, מכינים את הלוח:
def main():
    start_bool = True
    dungeon = game_field.generate_random_dungeon_grass(GRID_ROWS, GRID_COLS)
    dungeon_mines = game_field.generate_random_dungeon_mines(GRID_ROWS, GRID_COLS)
    state = {'state': game_consts.RUNNING_STATE}
    player_r, player_c = 1, 1
    # ניקוי וציור רקע: בכל פריים מחדש, מנקים את המסך עם צבע הרקע ומציירים את שכבת הדשא.
    while state['state'] == game_consts.RUNNING_STATE:
        game_screen.fill(COLOR_PANEL)
        Screen.draw_grass(dungeon)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state['state'] = game_consts.LOST_STATE
            # אם נלחץ מספר (1 עד 9) – רושמים את הזמן הנוכחי של הלחיצה כדי למדוד כמה זמן היא נמשכת.
            elif event.type == pygame.KEYDOWN:
                # לבדוק אם נלחץ מקש
                if event.key in NUMBER_KEYS:
                    key_press_times[event.key] = pygame.time.get_ticks()
                # כיוון תנועה לפי החצים במקלדת (dr = שינוי שורה, dc = שינוי עמודה).
                dr, dc = 0, 0
                if event.key == pygame.K_UP:
                    dr = -1
                elif event.key == pygame.K_DOWN:
                    dr = 1
                elif event.key == pygame.K_LEFT:
                    dc = -1
                elif event.key == pygame.K_RIGHT:
                    dc = 1
                # מקש Enter (ראיית לילה): חושף את רשת המשבצות והמוקשים, מציג את החייל במצב לילה, ומשהה את המשחק לשנייה אחת
                elif event.key == pygame.K_RETURN:
                    game_screen.fill(COLOR_PANEL)
                    Screen.draw_grid_lines(dungeon)
                    Screen.draw_mines(dungeon_mines)
                    Screen.draw_night_player(player_c, player_r)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                # אם החייל עלה על מוקש, הסטטוס משתנה ל-LOST_STATE, מוצגת הודעת הפסד ל-3 שניות והמשחק מסתיים.
                if dr != 0 or dc != 0:
                    player_r, player_c, new_state = soldier.move_player(dungeon_mines, player_r, player_c, dr, dc)
                    state['state'] = new_state
                    if state['state'] == game_consts.LOST_STATE:
                        game_screen.fill((0, 0, 0))
                        Screen.draw_lose_message()
                        pygame.display.flip()
                        pygame.time.wait(3000)
            # בדוק אם זה מספר ולחשב את הזמן
            elif event.type == pygame.KEYUP:
                if event.key in NUMBER_KEYS and event.key in key_press_times:
                    duration_ms = pygame.time.get_ticks() - key_press_times.pop(event.key)
                    duration_sec = duration_ms / 1000.0
                    slot_number = NUMBER_KEYS[event.key]
                    # short press (1 second or less) = save
                    if duration_sec <= 1.0:
                        database.save_game_state(slot_number, (player_r, player_c), dungeon_mines, dungeon
                        )
                        print(f"Saved game to slot {slot_number}")
                    # long press (more than 1 second) = load
                    else:
                        loaded = database.load_game_state(slot_number)
                        if loaded:
                            player_r, player_c = loaded["soldier_pos"]
                            dungeon_mines = loaded["mines"]
                            dungeon = loaded["grasses"]
                            print(f"Loaded game from slot {slot_number}")
        if state['state'] == game_consts.WIN_STATE:
            game_screen.fill((0, 0, 0))
            Screen.draw_win_message()
            pygame.display.flip()
            pygame.time.wait(3000)
        Screen.draw_flag()
        Screen.draw_player(player_c, player_r)
        pygame.display.flip()
        if start_bool:
            Screen.draw_welcome_message()
            pygame.display.flip()
            pygame.time.wait(1000)
            start_bool = False
        clock.tick(30)
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()