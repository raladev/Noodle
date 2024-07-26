from dataclasses import dataclass

import uuid

from models import constants


@dataclass(kw_only=True)
class Request:
    method: str = None
    id: str = str(uuid.uuid1())


@dataclass
class AddUserRequest(Request):
    name: str
    surname: str
    phone: str
    age: int

    def __post_init__(self):
        if self.method is None:
            self.method = constants.ADD_METHOD


@dataclass
class UpdateUserRequest(Request):
    name: str
    surname: str
    phone: str
    age: int

    def __post_init__(self):
        if self.method is None:
            self.method = constants.UPDATE_METHOD


@dataclass
class DeleteUserRequest(Request):
    phone: str

    def __post_init__(self):
        if self.method is None:
            self.method = constants.DELETE_METHOD


@dataclass
class SelectUserRequest(Request):
    name: str | None = None
    surname: str | None = None
    phone: str | None = None

    def __post_init__(self):
        if self.method is None:
            self.method = constants.SELECT_METHOD
        # TODO: add check only one parameter set
