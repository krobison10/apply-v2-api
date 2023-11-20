from ..config import *


class Interview:
    conn: DBConnection = None

    iid: int = None
    aid: int = None

    date: datetime = None
    modality: int = None
    location: str = None
    created_at: datetime = None
    updated_at: datetime = None

    application: Application = None

    def __init__(self):
        self.conn = DBConnection()

    def get(self):
        pass

    def update_edit_timestamp(self):
        pass

    def update(self, keep_updated_at=False):
        pass

    def save(self):
        pass

    def delete(self):
        pass
