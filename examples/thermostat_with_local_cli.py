#pylint: disable=wrong-import-position
import asyncio
import sys

sys.path.append('../chili_pad_with_thermostat')
from chili_pad_with_thermostat.thermostat import Thermostat
from chili_pad_with_thermostat.temp_program import TempProgram
from chili_pad_with_thermostat.cli import Cli
from chili_pad_with_thermostat.thermostat_rpc_handler import ThermostatRpcHandler

async def main():
    temp_program = TempProgram('/home/pi/chili_pad_with_thermostat/data/temp_profile.yml')
    thermo = Thermostat(temp_program=temp_program)
    command_handler = ThermostatRpcHandler(thermo)
    cli = Cli(command_handler.handle_command)
    await asyncio.gather(thermo.run(), cli.run())

asyncio.run(main())
