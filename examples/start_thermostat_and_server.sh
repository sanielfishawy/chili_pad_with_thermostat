#! /bin/bash
source ./venv/bin/activate
nohup python examples/thermostat_with_json_rpc_server.py &
echo '*** STARTED ***'
echo To terminate type: kill $!
echo