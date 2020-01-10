#pylint: disable=invalid-name

import smbus2
import bme280

class TemperatureSense:
    '''
    Wrapper for BME280 temerature sensor which uses RPi.BME280 driver.
    '''

    DEFAULT_PORT = 1
    DEFAULT_ADDRESS = 0x76

    def __init__(
            self,
            port=DEFAULT_PORT,
            address=DEFAULT_ADDRESS,
    ):
        self.port = port
        self.address = address
        self.bus = smbus2.SMBus(self.port)


    def get_temp_data(self):
        return bme280.sample(self.bus, self.address)

    def to_farheheit(self, deg_c):
        return 32 + 9 * deg_c/5

    def get_temp_fahrenheit(self):
        return self.to_farheheit(self.get_temp_data().temperature)