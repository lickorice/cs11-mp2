from data import db_helper

class PlayerDB(db_helper.DBHelper):
    def __init__(self):
        self.database_path = "data/db/players.db"
        self.is_logged = False

    def add_player(self, name, level, score):
        self.insert_row(
            "players",
            user_name=name, 
            user_level=level,
            user_score=score
            )
    
    def get_players(self):
        return self.fetch_all_rows(
            "players")