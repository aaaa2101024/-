"""自機センサの動作テスト"""
import smbus2 as smbus
import time

bus = smbus.SMBus(1)

MCP23017_ADDRESS = 0x20

IODIRA = 0x00
IODIRB = 0x01
GPIOA = 0x12
GPIOB = 0x13

bus.write_byte_data(MCP23017_ADDRESS, IODIRA, 0x00)
bus.write_byte_data(MCP23017_ADDRESS, IODIRB, 0xFF)
GPPUB = 0x0D  # プルアップ設定レジスタ
bus.write_byte_data(MCP23017_ADDRESS, GPPUB, 0x00)  # プルアップ無効
#bus.write_byte_data(MCP23017_ADDRESS, GPIOA, 0b11111110)
# bus.write_byte_data(MCP23017_ADDRESS, GPIOB, 0b11111111)

"""
gpiob_state = bus.read_byte_data(MCP23017_ADDRESS,GPIOB)
print(gpiob_state)
print(hex(gpiob_state))
"""
try:
    while True:
        gpiob_state = bus.read_byte_data(MCP23017_ADDRESS,GPIOB)
        print(gpiob_state)
        print(hex(gpiob_state))
    
        for i in range(8):
            pin_state = (gpiob_state >> i) & 1
            print(f"GPB{i}: {'HIGH' if pin_state else 'LOW'}")
        if gpiob_state == 0b00000001 :
            print("豆電球 ON")
            bus.write_byte_data(MCP23017_ADDRESS, GPIOA, 0b11111110)
        else:
            bus.write_byte_data(MCP23017_ADDRESS, GPIOA, 0b00000000)
            print("豆電球off")
except KeyboardInterrupt:
    bus.write_byte_data(MCP23017_ADDRESS, GPIOA, 0b00000000)
finally:
    bus.write_byte_data(MCP23017_ADDRESS, GPIOA, 0b00000000)

    

     
