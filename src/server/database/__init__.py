import sqlite3
import os
import sys
import hashlib

DB_FILENAME = "db.db"

def calculate_file_hash(path):
    with open(path,"rb") as f:
        bytes = f.read() # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest();
        return readable_hash

class Database:
    def __init__(self):
        # Create the database if it doesnt exist yet
        if not self.check_db():
            self.create_db()
        else:
            self.connect()

    def check_db(self):
        cwd = os.getcwd() 
        db_path = f'{cwd}/database/{DB_FILENAME}'
        #db_path = r'D:\Catena\src\server\database\db.db'
        return os.path.exists(db_path)

    def connect(self):
        cwd = os.getcwd()
        db_path = f'{cwd}/database/{DB_FILENAME}'
        #db_path = r'D:\Catena\src\server\database\db.db'
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.c = self.conn.cursor()

    def create_db(self):
        self.connect()
        self.c.execute('''
                  CREATE TABLE IF NOT EXISTS files 
                  ([ID] INTEGER PRIMARY KEY, [filename] TEXT, [version] TEXT, [creation_date] DATE, [added_date] DATE, [size] INT, [checksum] TEXT, [os] TEXT)
                  ''')
        self.conn.commit()

    def add_new_binary(self, filename, version, creation_date, added_date, size, checksum, os):
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
    print( db.get_by_hash('96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e') )
    #db.add_new_binary('test.exe', '1', '10-05-2022', '10-05-2022', 20, '96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e', 'WIN')
    #db.add_new_binary('test2.exe', '1', '10-05-2022', '10-05-2022', 20, '2f97c1842eb609905556cf784640abac357270c8a5c634f231c7ee5ae8b942b1', 'WIN')

