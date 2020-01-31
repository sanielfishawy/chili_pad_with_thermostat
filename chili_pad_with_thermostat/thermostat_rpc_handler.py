#pylint: disable=invalid-name, line-too-long
from chili_pad_with_thermostat.thermostat import Thermostat

class ThermostatRpcHandler:
    PROG = 'prog'
    THERMO = 'thermo'
    CP = 'cp'
    PID = 'pid'
    SENSE = 'sense'
    PWM = 'pwm'
    OBJECTS = [
        PROG,
        THERMO,
        CP,
        PID,
        SENSE,
        PWM,
    ]

    def __init__(
            self,
            thermostat: Thermostat,
    ):
        self.thermostat = thermostat



    def handle_command(self, *args):
        if len(args) == 1: # command has not yet been parsed.
            args = args[0].split(" ")
        if len(args) < 2:
            return "Command must be of the form: object method [params]"

        obj = args[0]
        meth = args[1]
        params = args[2:]

        if obj == self.__class__.PROG:
            obj = self.thermostat.temp_program
        elif obj == self.__class__.THERMO:
            obj = self.thermostat
        elif obj == self.__class__.CP:
            obj = self.thermostat.cp
        elif obj == self.__class__.PID:
            obj = self.thermostat.pid
        elif obj == self.__class__.SENSE:
            obj = self.thermostat.temp_sense
        elif obj == self.__class__.PWM:
            obj = self.thermostat.cp.pwm_power
        else:
            nl = '\n'
            msg = f'Unknown object: {obj}.  Try one of these:{nl}{nl.join(self.__class__.OBJECTS)}'
            return msg


        if not hasattr(obj, meth):
            good_methods = [func for func in dir(obj) if callable(getattr(obj, func)) and not func.startswith('_')]
            nl = '\n'
            return f"Unknown method: {meth}. Try one of these:{nl}{nl.join(good_methods)}"

        result = getattr(obj, meth)(*params)
        return result
