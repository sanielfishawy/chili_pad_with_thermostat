import asyncio
from aioconsole import ainput
from chili_pad_with_thermostat.thermostat import Thermostat
from chili_pad_with_thermostat.chili_logger import ChiliLogger

class Cli:
    '''
    Simple command line interface
    '''

    def __init__(
            self,
            thermostat=None,
    ):
        self.thermostat = thermostat or Thermostat()
        self.logger = ChiliLogger().get_logger()

    async def run(self):
        while True:
            command = await ainput('>>> ')
            self.handle_command(command)

    def handle_command(self, command):
        command = command.lower()

        if command == 'start':
            self.handle_start()
        elif command == 'debug':
            pass

    def handle_start(self):
        self.thermostat.start_program()
        self.logger.info('Program started at {self.thermostat.temp_program.start_date}')

