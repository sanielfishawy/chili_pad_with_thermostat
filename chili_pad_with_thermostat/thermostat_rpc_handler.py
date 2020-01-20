#pylint: disable=invalid-name, line-too-long
from chili_pad_with_thermostat.thermostat import Thermostat

class ThermostatRpcHandler:

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

        if obj == 'prog':
            obj = self.thermostat.temp_program
        elif obj == 'thermo':
            obj = self.thermostat
        elif obj == 'cp':
            obj = self.thermostat.cp
        elif obj == 'pid':
            obj = self.thermostat.pid
        elif obj == 'sense':
            obj = self.thermostat.temp_sense
        else:
            return f'Unknown object: {obj}'

        if not hasattr(obj, meth):
            good_methods = [func for func in dir(obj) if callable(getattr(obj, func)) and not func.startswith('_')]
            nl = '\n'
            return f"Unknown method: {meth} try one of these:{nl}{nl.join(good_methods)}"

        result = getattr(obj, meth)(*params)
        return result
