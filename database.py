import os
import pandas as pd

FILE_NAME = "game_database.csv"
COLUMNS = ["key", "soldier_pos", "mines", "grasses", "is_flag_reached"]

# להחזיר את טבלת השמירות המעודכנת ישירות לזיכרון של התוכנית.
def load_db():
    if not os.path.exists(FILE_NAME):
        empty_table = pd.DataFrame(columns=COLUMNS)
        empty_table.to_csv(FILE_NAME, index=False)
        return empty_table
    return pd.read_csv(FILE_NAME, dtype={"key": str})

# לשמור את נתוני המשחק הנוכחי בסלוט המבוקש (ולמחוק שמירה קודמת באותו סלוט אם הייתה).
def save_game_state(key, soldier_pos, mines, grasses, is_flag_reached=False):
    saves_table = load_db()
    k = str(key)

    # 1. מוחקים שמירה ישנה באותו סלוט (אם קיימת)
    saves_table = saves_table[saves_table["key"] != k]

    # 2. מוסיפים את השמירה החדשה לסוף הטבלה
    new_row = {
        "key": k,
        "soldier_pos": str(soldier_pos),
        "mines": str(mines),
        "grasses": str(grasses),
        "is_flag_reached": is_flag_reached,
    }
    saves_table.loc[len(saves_table)] = new_row

    saves_table.to_csv(FILE_NAME, index=False)
    print(f"Slot {k} saved successfully")

# למצוא שמירה לפי מספר סלוט ולהחזיר את כל הנתונים מוכנים להמשך המשחק.
def load_game_state(key):
    saves_table = load_db()
    k = str(key)

    # מחפשים את השורה המתאימה
    match = saves_table[saves_table["key"] == k]
    if match.empty:
        print(f"No save exists for slot {k}")
        return None

    # שולפים את הנתונים מהשורה שנמצאה
    row = match.iloc[0]
    return {
        "soldier_pos": (str(row["soldier_pos"])),
        "mines": (str(row["mines"])),
        "grasses": (str(row["grasses"])),
        "is_flag_reached": bool(row["is_flag_reached"]),
    }
# eval == שתפקידה לקחת מחרוזת של טקסט ולהריץ אותה כקוד לכל דבר