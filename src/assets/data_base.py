import sqlite3

class PlateNum_DB:
    def __init__(self, f_path):
        self.conn = sqlite3.connect(f_path)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS numbers(
                            data DATA,
                            number TEXT,
                            city TEXT,
                            first_name TEXT,
                            second_name TEXT)""")

    def insert(self, item):
        self.cur.execute("""INSERT OR IGNORE INTO numbers VALUES(?,?,?,?,?)""", item)
        self.conn.commit()

    def read_all(self):
        self.cur.execute("""SELECT * FROM numbers""")
        rows = self.cur.fetchall()
        return rows

    def read_one(self, number):
        self.cur.execute("""SELECT * FROM numbers WHERE number=?""", (number,))
        row = self.cur.fetchone()
        return row

    def delete_one(self, number):
        self.cur.execute("""DELETE FROM numbers WHERE number=?""", (number,))
        self.conn.commit()


