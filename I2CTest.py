#配線を変更することで豆電球をOnOffさせる
import smbus2 as smbus
import time

bus = smbus.SMBus(1)

MCP23017_ADRESS = 0x20

IODIRA = 0x00
IODIRB = 0x01
GPIOA = 0x12
GPIOB = 0x13

bus.write_byte_data(MCP23017_ADRESS, IODIRA, 0x00)
bus.write_byte_data(MCP23017_ADRESS, IODIRB, 0xFF)

try:
    while True:
        gpiob_state = bus.read_byte_data(MCP23017_ADRESS, GPIOB)

        if gpiob_state & 0b00000001:
            print("豆電球ON")
            bus.write_byte_data(MCP23017_ADRESS, GPIOA, 0b11111110)
        else:
            print("豆電球OFF")
            bus.write_byte_data(MCP23017_ADRESS, GPIOA, 0b00000000)

        time.sleep(3)
except KeyboardInterrupt:
    print("豆電球OFF")
    bus.write_byte_data(MCP23017_ADRESS, GPIOA, 0x00)