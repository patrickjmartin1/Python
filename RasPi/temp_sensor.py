from dht11 import DHT11
import RPi.GPIO as gpio
from time import sleep

# initialize gpio
gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.cleanup()

def cel_to_fahr(temp_c):
    temp_f = (temp_c * 1.8) + 32
    return temp_f 

class Sensor(DHT11):
    def __init__(self, pin):
        super().__init__(pin)

    def read_data(self):
        result = self.read()
        if result.is_valid():
            result.temperature = cel_to_fahr(result.temperature)
        return result


if __name__ == "__main__":
    sensor = Sensor(pin=6)
    while True:
        result = sensor.read_data()
        if result.is_valid():
            print("Temperature: {}".format(result.temperature))
            print("Humidity: {}".format(result.humidity))
        else: 
            print("Error: {}".format(result.error_code))
        sleep(1)


