import gpiozero as gz
from time import sleep

led = gz.LED("6")

while True:
    led.on()
    sleep(2)
    led.off()
    sleep(2)

