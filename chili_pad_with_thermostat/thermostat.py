import asyncio
from chili_pad.driver import Driver as CP
from chili_pad_with_thermostat.pid import PID
from chili_pad_with_thermostat.temperature_sense import TemperatureSense
from chili_pad_with_thermostat.temp_program import TempProgram
import chili_pad_with_thermostat.chili_logger as cl

class Thermostat:
    DEFAULT_SET_POINT = 75

    def __init__(
            self,
            temp_program: TempProgram = None,
    ):
        self.cp = CP()
        self.cp.pump_on()
        self.temp_sense = TemperatureSense()
        self.temp_program = temp_program
        self.pid = PID(
            Kp=5,
            Ki=0.001,
            Kd=10,
            setpoint=(self.temp_program and self.temp_program.start_temp) or Thermostat.DEFAULT_SET_POINT,
            sample_time=0.5,
            output_limits=(-100,100),
            integral_start_threshold=4,
            integral_stop_threshold=.1,
        )
        self.logger = cl.ChiliLogger().get_logger()

    async def run(self):
        while True:
            temp = self.temp_sense.get_temp_fahrenheit()

            if self.temp_program:
                self.set_temp(self.temp_program.get_temp())

            power = self.pid(temp)

            self.cp.set_abs_power(power)
            self.logger.info(self.get_status_string(temp))
            await asyncio.sleep(2)

    def get_status_string(self, temp=None):
        temp = temp or self.temp_sense.get_temp_fahrenheit()
        txt = f'Set: {self.pid.setpoint} '
        txt += f'Temp: {temp:0.2f} {self.cp.get_heat_cool()} Power:{self.cp.get_power()} '
        txt += f'Components: {self.pid.components}'
        return txt

    def set_temp(self, temp):
        self.pid.setpoint = temp

    def get_set_point(self):
        return self.pid.setpoint

    def start_program(self):
        self.temp_program.start()