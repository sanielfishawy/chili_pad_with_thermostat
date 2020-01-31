#pylint: disable=invalid-name
import asyncio
from chili_pad.driver import Driver as CP
from chili_pad_with_thermostat.pid import PID
from chili_pad_with_thermostat.temperature_sense import TemperatureSense
from chili_pad_with_thermostat.temp_program import TempProgram
import chili_pad_with_thermostat.chili_logger as cl

class Thermostat:
    DEFAULT_SET_POINT = 75
    MODE_HEAT_AND_COOL = 0
    MODE_HEAT_ONLY = 1
    MODE_COOL_ONLY = 2

    def __init__(
            self,
            temp_program: TempProgram = None,
    ):
        self.logger = cl.ChiliLogger().get_logger()
        self.cp = CP()
        self.cp.pump_on()
        self.temp_sense = TemperatureSense()
        self.temp_program = temp_program
        self.pid = PID(
            Kp=50,
            Ki=0.005,
            Kd=100,
            setpoint=(self.temp_program and self.temp_program.get_temp()) or Thermostat.DEFAULT_SET_POINT,
            sample_time=0.5,
            output_limits=(-100, 100),
            integral_start_threshold=1,
            integral_stop_threshold=.05,
        )
        self.is_on = False

        self.set_mode(TempProgram.MODE_HEAT_AND_COOL)
        self.turn_off()

    async def run(self):
        while True:
            if self.is_on:
                temp = self.temp_sense.get_temp_fahrenheit()

                if self.temp_program:
                    self.set_temp(self.temp_program.get_temp())
                    self.set_mode(self.temp_program.get_mode())

                power = self.pid(temp)

                self.cp.set_abs_power(power)
                self.logger.info(self.get_status_string(temp))

            await asyncio.sleep(2)

    def get_status_string(self, temp=None):
        temp = temp or self.temp_sense.get_temp_fahrenheit()
        txt = f'Set: {self.pid.setpoint:0.2f} '
        txt += f'Temp: {temp:0.2f} {self.cp.get_heat_cool()} Power:{self.cp.get_power()} '
        txt += f'Components: {[round(component, 2) for component in self.pid.components]} '
        txt += f'Limits: {self.pid.output_limits}'
        return str(txt)

    def set_temp(self, temp):
        self.pid.setpoint = temp

    def get_set_point(self):
        return self.pid.setpoint

    def start_program(self):
        self.turn_on()
        self.temp_program.reset()
        self.temp_program.start()
        self.logger.info('temp_program: started')
        return 'started'

    def turn_off(self):
        self.is_on = False
        self.cp.off()
        self.cp.set_abs_power(0)
        self.cp.pump_off()
        return 'off'

    def turn_on(self):
        self.is_on = True
        self.cp.pump_on()
        return 'on'

    def get_is_on(self):
        return self.is_on

    def set_mode(self, mode):
        if mode == TempProgram.MODE_HEAT_ONLY:
            self.pid.output_limits = (0,100)
        elif mode == TempProgram.MODE_COOL_ONLY:
            self.pid.output_limits = (-100, 0)
        elif mode == TempProgram.MODE_HEAT_AND_COOL:
            self.pid.output_limits = (-100, 100)
        else:
            raise KeyError(f'Unknown mode: {mode}')

    def get_mode(self):
        return self.pid.output_limits