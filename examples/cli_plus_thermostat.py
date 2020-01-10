import asyncio
import sys

sys.path.append('../chili_pad_with_thermostat')
from chili_pad_with_thermostat.thermostat import Thermostat
from chili_pad_with_thermostat.temp_program import TempProgram
from chili_pad_with_thermostat.cli import Cli

async def main():
    temp_program = TempProgram(
        start_temp=90,
        start_temp_hold_time=5,
        temp_drop_rate=.001,
    )

    # temp_program.start()

    thermo = Thermostat(
        # temp_program=temp_program,
    )
    cli = Cli(
        thermostat=thermo,
    )
    await asyncio.gather(thermo.run(), cli.run())


asyncio.run(main())
