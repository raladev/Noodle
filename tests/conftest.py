import os

import pytest
from dotenv import load_dotenv

from clients.sync_client import SyncClient
from helpers.service import ServiceHelper
from models import constants
from models.requests import AddUserRequest

load_dotenv()

HOST = os.environ.get("HOST", None)
BIN_BATH = os.environ.get("BIN_PATH", None)
assert HOST is not None, "HOST is not set as ENV var, abort"
assert BIN_BATH is not None, "BIN_BATH is not set as ENV var, abort"


@pytest.fixture()
def service(tmp_path, unused_tcp_port):
    service = ServiceHelper(HOST, str(unused_tcp_port), tmp_path.absolute(), BIN_BATH)
    service.start()
    yield service
    service.stop()


@pytest.fixture
def client(service):
    yield SyncClient(service.host, service.port)


@pytest.fixture
def user(client):
    # TODO: generate random values
    user = AddUserRequest(name="Roman", surname="Aladev", phone="8913", age=15)
    response = client.send_request(user)
    assert response.status == constants.SUCCESS_STATUS
    return user
    # TODO: delete user
