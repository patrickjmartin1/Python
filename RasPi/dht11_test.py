import dht11
import RPi.GPIO as gpio

# initialize gpio
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.cleanup()

sensor = dht11.DHT11(pin=6)

result = sensor.read()

if result.is_valid():
    print("Temperature: {}".format(result.temperature))
    print("Humidity: {}".format(result.humidity))
else: 
    print("Error: {}".format(result.error_code))


