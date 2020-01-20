#pylint: disable=wrong-import-position, invalid-name
import asyncio
import sys

sys.path.append('../chili_pad_with_thermostat')
from chili_pad_with_thermostat.cli import Cli
from chili_pad_with_thermostat.json_rpc_client import JsonRpcClient

if __name__ == '__main__':
    cli = Cli(JsonRpcClient.send_request)
    asyncio.run(cli.run())