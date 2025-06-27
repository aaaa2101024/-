'''
management.MCP23017_ADDRESS = 0x20

IODIRA = 0x00
IODIRB = 0x01
management.GPIOA = 0x12
GPIOB = 0x13

bus.write_byte_data(management.MCP23017_ADDRESS, IODIRA, 0x00)
bus.write_byte_data(management.MCP23017_ADDRESS, IODIRB, 0xFF)
GPPUB = 0x0D  # プルアップ設定レジスタ
bus.write_byte_data(management.MCP23017_ADDRESS, GPPUB, 0x00)  # プルアップ無効
#bus.write_byte_data(management.MCP23017_ADDRESS, management.GPIOA, 0b11111110)
# bus.write_byte_data(management.MCP23017_ADDRESS, GPIOB, 0b11111111)

gpiob_state = bus.read_byte_data(management.MCP23017_ADDRESS,GPIOB)
'''
# 複数人分の在室管理ができるように拡張
# listに書き換え
import redis.exceptions
import smbus2 as smbus
import time
import sqlite3
from datetime import datetime
import redis

class Management:
     def __init__(self):
          self.bus = smbus.SMBus(1)
          self.MCP23017_ADDRESS = 0x20
          self.IODIRA = 0x00
          self.IODIRB = 0x01
          self.GPIOA = 0x12
          self.GPIOB = 0x13
          self.GPPUB = 0x0D  # プルアップ設定レジスタ
          self.bus.write_byte_data(self.MCP23017_ADDRESS, self.IODIRA,0x00)
          self.bus.write_byte_data(self.MCP23017_ADDRESS, self.IODIRB, 0xFF)
          self.bus.write_byte_data(self.MCP23017_ADDRESS,self.GPPUB,0x00)
          self.gpiob_state = self.bus.read_byte_data(self.MCP23017_ADDRESS,self.GPIOB)

class DB:
     def __init__(self, db_path="./../src/data/testDB.db"):
          self.db_path = db_path
          with self._get_connection() as conn:
              cursor = conn.cursor()
              cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL UNIQUE,
                    status TEXT NOT NULL,
                    time TEXT NOT NULL
                );
            """)
          conn.commit()
     def _get_connection(self):
        return sqlite3.connect(self.db_path)

     def update_status(self, name: str, status: str):
         now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         sql = "UPDATE attendance SET status = ?, time = ? WHERE name = ?"
         
         try:
             with self._get_connection() as conn:
                 cursor = conn.cursor()
                 cursor.execute(sql, (status, now_str, name))
                 conn.commit()
                 print(f"Updated DB: {name} is now {status}")
                 return True
         except sqlite3.Error as e:
             print(f"DB Error: {e}")
             return False
    #  def reflect_in(self,name):
    #     now = datetime.now()
    #     now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    #     self.cursor.execute("UPDATE attendance SET status = \"在室\" WHERE name = \"" + name + "\";")
    #     self.cursor.execute("UPDATE attendance SET time = \"" + now_str + "\" WHERE name = \"" + name + "\";")
    #     self.conn.commit()
    #  def reflect_ref(self,name):
    #     now = datetime.now()
    #     now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    #     self.cursor.execute("UPDATE attendance SET status = \"休憩中\" WHERE name = \"" + name + "\";")
    #     self.cursor.execute("UPDATE attendance SET time = \"" + now_str + "\" WHERE name = \"" + name + "\";")
    #     self.conn.commit()
    #  def reflect_out(self,name):
    #     now = datetime.now()
    #     now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    #     self.cursor.execute("UPDATE attendance SET status = \"退室\" WHERE name = \"" + name + "\";")
    #     self.cursor.execute("UPDATE attendance SET time = \"" + now_str + "\" WHERE name = \"" + name + "\";")
    #     self.conn.commit()
    #  def show(self):
    #       self.cursor.execute("SELECT * FROM attendance;")
    #       self.rows = self.cursor.fetchall()
    #       for row in self.rows:
    #            print(row)
    
def main():
    managemant = Management()
    db = DB()
    
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    REDIS_CHANNEL = "attendance_channel"
    
    name_list = ["nojiri", "shiomi", "aaaaa"]
    
    last_known_state = -1
    
    print("センサーの監視を開始します。終了するにはCtrl+Cを押してください")
    try:
        while True:
            current_state = managemant.bus.read_byte_data(managemant.MCP23017_ADDRESS, managemant.GPIOB)
            
            if current_state != last_known_state:
                
                for i in range(len(name_list)):
                    user_bit_pos = i * 2

                    mask = 0b11 << user_bit_pos

                    user_current_bits = (current_state & mask) >> user_bit_pos
                    user_last_bits = (last_known_state & mask) >> user_bit_pos

                    if user_current_bits != user_last_bits:
                        user_name = name_list[i]
                        new_status = ""

                        if user_current_bits == 0b00:
                            new_status = "退室"
                        elif user_current_bits == 0b01:
                            new_status = "休憩中"
                        elif user_bit_pos == 0b10:
                            new_status = "在室"
                        else:
                            new_status = "不明"
                        if db.update_status(user_name, new_status):
                            try:
                                redis_client.publish(REDIS_CHANNEL, "updated")
                                print(f"Published 'updated' message to Redis channel '{REDIS_CHANNEL}'.")
                            except redis.exceptions.ConnectionError as e:
                                print(f"Redis connection error: {e}")
                last_known_state = current_state
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stop")
    finally:
        pass

if __name__ == "__main__":
    main()

# management = Management()
# db = DB()

# print(management.gpiob_state)
# print(hex(management.gpiob_state))

# name_list = ["nojiri","shiomi","aaaaaa"]

# '''
# 00 => 退室
# 01 => 休憩
# 10 => 在室
# '''
# try:
#     pre = (1 << 16)
#     while True:
#         gpiob_state = management.bus.read_byte_data(management.MCP23017_ADDRESS,management.GPIOB)
#         # print(gpiob_state)
#         # print(hex(gpiob_state))
    
#         for i in range(8):
#             pin_state = (gpiob_state >> i) & 1
#             print(f"GPB{i}: {'HIGH' if pin_state else 'LOW'}")
#         str_gpiob = ""
#         str_pre = ""
#         for i in range (8):
#             if gpiob_state & 1 << i:
#                 str_gpiob += '1'
#             else:
#                 str_gpiob += '0'
        
#         for i in range (8):
#             if pre & 1 << i:
#                 str_pre += '1'
#             else:
#                 str_pre += '0'
        
#         for i in range(3):
#             if str_gpiob[i * 2:(i + 1) * 2] != str_pre[i * 2:(i + 1) * 2]:
#                 print(str_gpiob)
#                 print(str_pre)
#                 j = i * 2
#                 # print(1 << j)
#                 print(i)
#                 if gpiob_state & (1 << j):
#                     # print(name_list[i])
#                     # print(i)
#                     db.reflect_ref(name_list[i])
#                     pre = gpiob_state
#                 elif gpiob_state & (10 << j):
#                     # print(name_list[i])
#                     # print(i)
#                     db.reflect_in(name_list[i])
#                     pre = gpiob_state
#                 else:
#                     # print(name_list[i])
#                     # print(i)
#                     db.reflect_out(name_list[i])
#                     pre = gpiob_state
        
#         time.sleep(1)
# except KeyboardInterrupt:
#     management.bus.write_byte_data(management.MCP23017_ADDRESS, management.GPIOA, 0b00000000)
# finally:
#     management.bus.write_byte_data(management.MCP23017_ADDRESS, management.GPIOA, 0b00000000)

