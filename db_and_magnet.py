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
# DBと磁石実装
import smbus2 as smbus
import time
import sqlite3

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
    

management = Management()
db = DB()

print(management.gpiob_state)
print(hex(management.gpiob_state))

try:
    while True:
        gpiob_state = management.bus.read_byte_data(management.MCP23017_ADDRESS,management.GPIOB)
        print(gpiob_state)
        print(hex(gpiob_state))
    
        for i in range(8):
            pin_state = (gpiob_state >> i) & 1
            print(f"GPB{i}: {'HIGH' if pin_state else 'LOW'}")
        if gpiob_state == 0b00000001 :
            db.reflect_in()
            management.bus.write_byte_data(management.MCP23017_ADDRESS, management.GPIOA, 0b11111110)
        else:
            management.bus.write_byte_data(management.MCP23017_ADDRESS, management.GPIOA, 0b00000000)
            db.reflect_out()
except KeyboardInterrupt:
    management.bus.write_byte_data(management.MCP23017_ADDRESS, management.GPIOA, 0b00000000)
finally:
    management.bus.write_byte_data(management.MCP23017_ADDRESS, management.GPIOA, 0b00000000)

