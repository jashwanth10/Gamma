from minidatabase import minidb


class Database:

    def __init__(self, path="database/db.minidb"):
        self.path = path
        self.db = minidb.connect(path)

    def insert(self, key, value):
        self.db.append(key, value)
        self.db.commit()
        return

    def query(self, key):
        records = self.db.get(key)
        return records

