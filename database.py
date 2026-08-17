import os
import ast
import pandas as pd
import game_consts
FILE_NAME = "game_database.csv"
COLUMNS = ["key", "soldier_pos", "mines", "grasses", "is_flag_reached"]
# להחזיר את טבלת השמירות המעודכנת ישירות לזיכרון של התוכנית.
def load_db():
    if not os.path.exists(FILE_NAME):
        empty_table = pd.DataFrame()
        empty_table.to_csv(FILE_NAME)
        return empty_table
    return pd.read_csv(FILE_NAME)

# לשמור את נתוני המשחק הנוכחי בסלוט המבוקש (ולמחוק שמירה קודמת באותו סלוט אם הייתה).
def save_game_state(key, soldier_pos, mines, grasses, is_flag_reached=False):
    saves_table = load_db()
    k = key

    #  מוחקים שמירה ישנה באותו סלוט (אם קיימת)
    drop_indices = []

    for idx, row in saves_table.iterrows():
        if row["key"] != k:
            drop_indices.append(idx)

    saves_table = saves_table.drop(drop_indices)

    #  מוסיפים את השמירה החדשה לסוף הטבלה
    new_row = {
        "key": k,
        "soldier_pos": soldier_pos,
        "mines": mines,
        "grasses": grasses,
        "is_flag_reached": is_flag_reached,
    }
    saves_table.loc[len(saves_table)] = new_row

    saves_table.to_csv(FILE_NAME, index=False)
    print(f"Slot {k} saved successfully")

# למצוא שמירה לפי מספר סלוט ולהחזיר את כל הנתונים מוכנים להמשך המשחק.
def load_game_state(key):
    saves_table = load_db()
    k = key
    #  מוחקים שמירה ישנה באותו סלוט (אם קיימת)
    match = []

    # מחפשים את השורה המתאימה   `
    for idx, row in saves_table.iterrows():
        if row["key"] == k:
            match.append(idx)
    saves_table = saves_table.loc[match]
    if saves_table.empty:
        print(f"No save exists for slot {k}")
        return None

    # שולפים את הנתונים מהשורה שנמצאה
    row = saves_table.loc[0]
    print(type(row["soldier_pos"]))
    return {
        # literal_eval() - safely evaluate a string containing a Python literal structure.
        "soldier_pos": ast.literal_eval(row["soldier_pos"]),
        "mines": ast.literal_eval(row["mines"]),
        "grasses": ast.literal_eval(row["grasses"]),
        "is_flag_reached": bool(row["is_flag_reached"]),
    }
