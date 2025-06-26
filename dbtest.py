#DBをpythonを使って書き換える
import smbus2 as smbus
import time
import sqlite3

class DB:
     def __init__(self):
          self.conn = sqlite3.connect('testDB.db')
          self.cursor = self.conn.cursor()
          self.create_table_sql = """
            CREATE TABLE IF NOT EXISTS attendance (
                name TEXT NOT NULL,
                status TEXT NOT NULL,
                time TEXT NOT NULL
            );
            """
          self.cursor.execute(self.create_table_sql)
     def reflect_in(self):
        self.cursor.execute("UPDATE attendance SET status = \"在室\" WHERE name = \"nojiri\";")
        self.conn.commit()
     def reflect_out(self):
        self.cursor.execute("UPDATE attendance SET status = \"退室\" WHERE name = \"nojiri\";")
        self.conn.commit()
     def show(self):
          self.cursor.execute("SELECT * FROM attendance;")
          self.rows = self.cursor.fetchall()
          for row in self.rows:
               print(row)
    
db = DB()


bus = smbus.SMBus(1)

db.reflect_out()
db.show()