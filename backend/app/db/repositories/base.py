from databases import Database


class BaseRepository:
    """
    A reference to the database connection
    """
    def __init__(self, db: Database) -> None:
        self.db = db