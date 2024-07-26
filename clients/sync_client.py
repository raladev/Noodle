from websockets.sync.client import connect
from models.requests import AddUserRequest, SelectUserRequest, DeleteUserRequest

import json
from dataclasses import is_dataclass, asdict

from models.responses import Response


class DataclassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            # lambda function skips all dict pairs with None Value
            return asdict(
                o, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
            )
        return super().default(o)


class SyncClient:
    def __init__(self, host, port, protocol: str = "ws"):
        self.timeout = 5
        self.ws = connect(f"{protocol}://{host}:{port}")

    def __del__(self):
        self.ws.close()

    def send_request(
        self, command: AddUserRequest | DeleteUserRequest | SelectUserRequest
    ):
        self.ws.send(json.dumps(command, cls=DataclassJSONEncoder))
        # TODO: Add cycle to find message with identical id
        json_msg = self.recv_msg()

        response = Response.from_dict(json_msg)
        assert (
            command.id == response.id
        ), f"response id ({response.id}) differs from request id ({command.id}), something wrong"
        return response

    def send_raw_msg(self, msg: str):
        self.ws.send(json.dumps(msg))

    def recv_msg(self):
        try:
            raw_msg = self.ws.recv(self.timeout)
        except TimeoutError:
            assert False, "Did not get any response messages from ws, something wrong"
        return json.loads(raw_msg)
