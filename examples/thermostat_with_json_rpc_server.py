#pylint: disable=wrong-import-position, invalid-name
import threading
import asyncio
import sys

sys.path.append('../chili_pad_with_thermostat')
from chili_pad_with_thermostat.thermostat import Thermostat
from chili_pad_with_thermostat.temp_program import TempProgram
from chili_pad_with_thermostat.json_rpc_server import JsonRpcServer
from chili_pad_with_thermostat.thermostat_rpc_handler import ThermostatRpcHandler

temp_program = TempProgram('/home/pi/chili_pad_with_thermostat/data/temp_profile.yml')
thermostat = Thermostat(temp_program=temp_program)
thermostat_rpc_handler = ThermostatRpcHandler(thermostat)
JsonRpcServer.set_rpc_handler(thermostat_rpc_handler.handle_command)

srv = threading.Thread(target=JsonRpcServer.run_server)
srv.start()
asyncio.run(thermostat.run())
