import os
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpcserver import method, dispatch

from chili_pad_with_thermostat.thermostat_rpc_handler import ThermostatRpcHandler

class JsonRpcServer:

    @staticmethod
    def dummy_handler(obj, meth, params):
        return [obj, meth, params]

    rpc_handler = staticmethod(dummy_handler)

    @staticmethod
    def set_rpc_handler(handler: ThermostatRpcHandler):
        JsonRpcServer.rpc_handler = staticmethod(handler)

    @staticmethod
    @method
    def handle_request(*args):
        print(args)
        return JsonRpcServer.rpc_handler(*args)

    @staticmethod
    @Request.application
    def application(request):
        response = dispatch(request.data.decode())
        return Response(str(response), response.http_status, mimetype="application/json")

    @staticmethod
    def get_ip():
        f = os.popen('hostname -I')
        return f.read().strip()

    @staticmethod
    def run_server():
        run_simple(JsonRpcServer.get_ip(), 5000, JsonRpcServer.application)
