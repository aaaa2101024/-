import RPi.GPIO as GPIO
import time
LED = 17
wait = 1
GPIO.setmode(GPIO.BCM)

GPIO.setup(LED, GPIO.OUT)

while True:
    GPIO.output(LED, GPIO.HIGH)
    time.sleep(wait)
    GPIO.output(LED,GPIO.LOW)
    time.sleep(wait)