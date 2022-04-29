import sqlite3
import os
import sys

DB_FILENAME = "db.db"

class Database:
    def __init__(self):
        # Create the database if it doesnt exist yet
        if not self.check_db():
            self.create_db()
        else:
            self.connect()

    def check_db(self):
        cwd = os.path.realpath(__file__)
        cwd = cwd[:cwd.find(sys.argv[0])]
        db_path = f'{cwd}/{DB_FILENAME}'
        return os.path.exists(db_path)

    def connect(self):
        cwd = os.path.realpath(__file__)
        cwd = cwd[:cwd.find(sys.argv[0])]
        db_path = f'{cwd}/{DB_FILENAME}'
        self.conn = sqlite3.connect(db_path, check_same_thread=False) 
        self.c = self.conn.cursor()

    def create_db(self):
        self.connect()
        self.c.execute('''
                  CREATE TABLE IF NOT EXISTS files 
                  ([ID] INT PRIMARY KEY, [filename] TEXT, [version] TEXT, [creation_date] DATE, [added_date] DATE, [size] INT, [checksum] TEXT, [os] TEXT)
                  ''')
        self.conn.commit()

    def add_new_binary(self, filename, version, creation_date, added_date, size, checksun, os):
        command = 'INSERT INTO files(filename, version, creation_date, added_date, size, checksum, os) VALUES (?, ?, ?, ?, ?, ?, ?)'
        self.c.execute(command, (filename, version, creation_date, added_date, size, checksum, os))
        self.conn.commit()
        return True

    def get_all(self):
        self.c.execute(f"SELECT * FROM files")
        data = self.c.fetchall()
        return data

    def get_by_hash(self, h):
        self.c.execute("SELECT * FROM files WHERE checksum=:h", {"h": h})
        data = self.c.fetchall()
        return data

    def get_by_name(self, name):
        self.c.execute("SELECT * FROM files WHERE filename=:name", {"name": name})
        data = self.c.fetchall()
        return data


if __name__ == "__main__":
    db = Database()

