# import json
import requests

class JsonRpcClient:
    SERVER_URL = 'http://sanichili.local:5000'

    BASE_JSON_REQUEST = {
        'method': 'handle_request',
        'jsonrpc': '2.0',
        'id': 0,
    }

    def __init__(
            self,
    ):
        pass

    @staticmethod
    def get_json_request_from_command(command):
        res = JsonRpcClient.BASE_JSON_REQUEST
        res['params'] = command.split(' ')
        return res

    @staticmethod
    def send_request(command):
        response = requests.post(
            JsonRpcClient.SERVER_URL,
            json=JsonRpcClient.get_json_request_from_command(command)
            ).json()

        if 'result' in response.keys():
            return response['result']
        else:
            return response

