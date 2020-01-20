from aioconsole import ainput

class Cli:
    '''
    Simple command line interface
    '''

    def __init__(
            self,
            command_handler,
    ):
        self.command_handler = command_handler

    async def run(self):
        while True:
            command = await ainput('>>> ')
            print(self.command_handler(command))

