from dataclasses import dataclass
from typing import List


@dataclass
class User:
    name: str
    surname: str
    phone: str
    age: int

    @classmethod
    def from_dict(cls, data: dict):
        # TODO: collect list from class attributes
        class_set = set(["name", "surname", "phone", "age"])
        response_set = set(data.keys())
        assert len(response_set) == len(
            data.keys()
        ), f"There is duplicate fields in response: {data.keys()}"
        assert (
            response_set.difference(class_set) == set()
        ), f"Response has unexpected fields ({data})"

        return cls(
            name=data.get("name", None),
            surname=data.get("surname", None),
            phone=data.get("phone", None),
            age=data.get("age", None),
        )


# TODO : divide to separate responses
@dataclass(kw_only=True)
class Response:
    method: str | None
    id: str | None
    status: str | None
    reason: str | None
    users: List[User] | None

    @classmethod
    def from_dict(cls, data: dict):
        # TODO: collect list from class attributes
        class_set = set(["method", "id", "status", "reason", "users"])
        response_set = set(data.keys())
        assert len(response_set) == len(
            data.keys()
        ), f"There is duplicate fields in response: {data.keys()}"
        assert (
            response_set.difference(class_set) == set()
        ), f"Response has unexpected fields ({data})"

        return cls(
            method=data.get("method", None),
            id=data.get("id", None),
            status=data.get("status", None),
            reason=data.get("reason", None),
            users=data.get("users", None),
        )
