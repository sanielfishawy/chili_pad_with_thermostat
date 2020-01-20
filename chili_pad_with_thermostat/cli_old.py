from aioconsole import ainput
from chili_pad_with_thermostat.thermostat import Thermostat

class Cli:
    '''
    Simple command line interface
    '''

    def __init__(
            self,
            thermostat=None,
            command_handler=None,
    ):
        self.thermostat = thermostat or Thermostat()
        self.command_handler = command_handler or self.handle_command

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

