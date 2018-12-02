from data import db_helper

class PlayerDB(db_helper.DBHelper):
    """
    A more specific class that inherits the :class:`.DBHelper` class.
    """
    def __init__(self):
        self.database_path = "data/db/players.db"
        self.is_logged = False

    def add_player(self, name, level, score):
        """
        Adds a player to the database.

        Args:
            name (str): Player name.
            level (int): Player level.
            score (int): Player score.
        """
        self.insert_row(
            "players",
            user_name=name, 
            user_level=level,
            user_score=score
            )
    
    def get_players(self):
        """Returns raw queries of all players."""
        return self.fetch_all_rows(
            "players")