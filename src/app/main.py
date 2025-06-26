from fastapi import FastAPI
from api import attendance

# try :
#     with sqlite3.connect('../data/testDB.db') as conn:
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
    
#         cursor.execute("SELECT * FROM attendance")
#         rows_from_db = cursor.fetchall()

# except sqlite3.Error as e:
#     print(f"データベースエラー: {e}")
#     rows_from_db = []

app = FastAPI()

app.include_router(attendance.router)

