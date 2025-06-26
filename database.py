# データベースをpythonで書くテスト
import sqlite3

conn = sqlite3.connect('testDB.db')

cursor = conn.cursor()
create_table_sql = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT UNIQUE
) ;
"""

cursor.execute(create_table_sql)

user_data = ('Shiomi', 70, 'shiomi.inf@shizuoka.ac.jp')
insert_sql = "INSERT INTO users (name, age, email) VALUES(?,?,?)"
cursor.execute(insert_sql, user_data)

conn.commit()



