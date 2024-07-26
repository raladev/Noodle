import pytest

from helpers.utils import assert_users_equal
from models import constants
from models.requests import AddUserRequest, SelectUserRequest
import allure

from models.responses import User, Response


# TODO: A lot of copy paste, could be optimized, but not now -_-
class TestAddUserValidation:

    @pytest.mark.parametrize(
        "user",
        [
            AddUserRequest(name="Roman", surname="Aladev", phone="1", age=1),
            AddUserRequest(name="R`Ar el-tiar!", surname="Aladev", phone="0", age=0),
            AddUserRequest(name="Роман", surname="Aladev", phone="0", age=0),
            AddUserRequest(name="ءآأؤإئا", surname="Aladev", phone="0", age=0),
            AddUserRequest(name='ER\r\nAr"i¬!!a', surname="Aladev", phone="0", age=0),
            AddUserRequest(name="", surname="Aladev", phone="0", age=0),
            pytest.param(
                AddUserRequest(name="a" * 905, surname="Aladev", phone="0", age=0),
                marks=pytest.mark.skip(
                    reason="buffer overflow (based on logs) when whole message is bigger then > 1024 symbols"
                ),
            ),
        ],
        ids=[
            "Common name",
            "Uncommon name",
            "Cirillic name",
            "Arabic name",
            "Spec symbols",
            "Empty String Name",
            "Too Long Name",
        ],
    )
    @allure.title("Check validation for name field (positive)")
    def test_name_validation_positive(self, client, user):
        with allure.step("Send Add User request"):
            add_user_req = user
            response = client.send_request(add_user_req)

        with allure.step("Check operation succeed"):
            assert (
                response.status == constants.SUCCESS_STATUS
            ), f"Status is not Successful, {response}"
            assert (
                response.method == constants.ADD_METHOD
            ), f"Response Method is different from Request Method, {response}"

        with allure.step("Perform select using user's phone number"):
            search_user_req = SelectUserRequest(phone=add_user_req.phone)
            response = client.send_request(search_user_req)

        # Note: It is better to query db directly to check such data
        with allure.step("Check user found and all fields filled correctly"):
            assert len(response.users) == 1, f"User not found, {response}"
            response_user = User.from_dict(response.users[0])
            assert_users_equal(response_user, add_user_req)

    @pytest.mark.parametrize(
        "user",
        [
            AddUserRequest(name=12, surname="Aladev", phone="0", age=0),
            AddUserRequest(name=-12.0, surname="Aladev", phone="0", age=0),
        ],
        ids=[
            "int Name",
            "float Name",
        ],
    )
    @allure.title("Check validation for name field (negative)")
    def test_name_validation_negative(self, client, user):
        with allure.step("Send Add User request"):
            add_user_req = user
            response = client.send_request(add_user_req)

        with allure.step("Check operation failed"):
            assert (
                response.status == constants.FAILURE_STATUS
            ), f"Status is Successful, {response}"
            assert (
                response.method == constants.ADD_METHOD
            ), f"Response Method is different from Request Method, {response}"
            assert response.reason is not None

    @pytest.mark.parametrize(
        "param",
        [" ", None],
        ids=[
            "No name field",
            "Name field is Null",
        ],
    )
    @allure.title("Check validation for name field (negative)")
    def test_name_validation_negative_raw_request(self, client, param):
        with allure.step("Send Add User request"):
            msg = {
                "method": "add",
                "id": "960d46a3-4b51-11ef-8600-e86a64efce12",
                "surname": "Aladev",
                "phone": "1",
                "age": 1,
            }

            if param is not None:
                msg["name"] = None

            client.send_raw_msg(msg)
            resp_json = client.recv_msg()
            response = Response.from_dict(resp_json)

        with allure.step("Check operation failed"):
            assert (
                response.status == constants.FAILURE_STATUS
            ), f"Status is Successful, {response}"
            assert (
                response.method == constants.ADD_METHOD
            ), f"Response Method is different from Request Method, {response}"
            assert response.reason is not None

    @pytest.mark.parametrize(
        "user",
        [
            AddUserRequest(surname="Roman", name="Roman", phone="1", age=1),
            AddUserRequest(surname="R`Ar el-tiar!", name="Roman", phone="0", age=0),
            AddUserRequest(surname="Роман", name="Roman", phone="0", age=0),
            AddUserRequest(surname="ءآأؤإئا", name="Roman", phone="0", age=0),
            AddUserRequest(surname='ER\r\nAr"i¬!!a', name="Roman", phone="0", age=0),
            AddUserRequest(surname="", name="Roman", phone="0", age=0),
        ],
        ids=[
            "Common surname",
            "Uncommon surname",
            "Cirillic surname",
            "Arabic surname",
            "Spec symbols in surname",
            "Empty String surname",
        ],
    )
    @allure.title("Check validation for surname field (positive)")
    def test_surname_validation_positive(self, client, user):
        with allure.step("Send Add User request"):
            add_user_req = user
            response = client.send_request(add_user_req)

        with allure.step("Check operation succeed"):
            assert (
                response.status == constants.SUCCESS_STATUS
            ), f"Status is not Successful, {response}"
            assert (
                response.method == constants.ADD_METHOD
            ), f"Response Method is different from Request Method, {response}"

        with allure.step("Perform select using user's phone number"):
            search_user_req = SelectUserRequest(phone=add_user_req.phone)
            response = client.send_request(search_user_req)

        # Note: It is better to query db directly to check such data
        with allure.step("Check user found and all fields filled correctly"):
            assert len(response.users) == 1, f"User not found, {response}"
            response_user = User.from_dict(response.users[0])
            assert_users_equal(response_user, add_user_req)

    @pytest.mark.parametrize(
        "user",
        [
            AddUserRequest(surname=12, name="Aladev", phone="0", age=0),
            AddUserRequest(surname=-12.0, name="Aladev", phone="0", age=0),
        ],
        ids=[
            "int surname",
            "float surname",
        ],
    )
    @allure.title("Check validation for surname field (negative)")
    def test_surname_validation_negative(self, client, user):
        with allure.step("Send Add User request"):
            add_user_req = user
            response = client.send_request(add_user_req)

        with allure.step("Check operation failed"):
            assert (
                response.status == constants.FAILURE_STATUS
            ), f"Status is Successful, {response}"
            assert (
                response.method == constants.ADD_METHOD
            ), f"Response Method is different from Request Method, {response}"
            assert response.reason is not None

    @pytest.mark.parametrize(
        "param",
        [" ", None],
        ids=[
            "No surname field",
            "Surname field is Null",
        ],
    )
    @allure.title("Check validation for surname field (negative)")
    def test_surname_validation_negative_raw_request(self, client, param):
        with allure.step("Send Add User request"):
            msg = {
                "method": "add",
                "id": "960d46a3-4b51-11ef-8600-e86a64efce12",
                "name": "Aladev",
                "phone": "1",
                "age": 1,
            }

            if param is not None:
                msg["surname"] = None

            client.send_raw_msg(msg)
            resp_json = client.recv_msg()
            response = Response.from_dict(resp_json)

        with allure.step("Check operation failed"):
            assert (
                response.status == constants.FAILURE_STATUS
            ), f"Status is Successful, {response}"
            assert (
                response.method == constants.ADD_METHOD
            ), f"Response Method is different from Request Method, {response}"
            assert response.reason is not None

    @pytest.mark.parametrize(
        "user",
        [
            AddUserRequest(surname="Aladev", name="Roman", phone="89135789924", age=1),
            AddUserRequest(surname="Aladev", name="Roman", phone="911", age=0),
            AddUserRequest(
                surname="Aladev", name="Roman", phone="8-913-579-22-22", age=0
            ),
            AddUserRequest(surname="Aladev", name="Roman", phone="4294967296", age=0),
        ],
        ids=[
            "Common phone",
            "Uncommon phone",
            "+ - ()",
            "> int32, >int64, >unsigned int",
        ],
    )
    @allure.title("Check validation for phone field (positive)")
    def test_phone_validation_positive(self, client, user):
        with allure.step("Send Add User request"):
            add_user_req = user
            response = client.send_request(add_user_req)

        with allure.step("Check operation succeed"):
            assert (
                response.status == constants.SUCCESS_STATUS
            ), f"Status is not Successful, {response}"
            assert (
                response.method == constants.ADD_METHOD
            ), f"Response Method is different from Request Method, {response}"

        with allure.step("Perform select using user's phone number"):
            search_user_req = SelectUserRequest(phone=add_user_req.phone)
            response = client.send_request(search_user_req)

        # Note: It is better to query db directly to check such data
        with allure.step("Check user found and all fields filled correctly"):
            assert len(response.users) == 1, f"User not found, {response}"
            response_user = User.from_dict(response.users[0])
            assert_users_equal(response_user, add_user_req)

    @pytest.mark.parametrize(
        "user",
        [
            AddUserRequest(surname="Aladev", name="Roman", phone=True, age=0),
            AddUserRequest(surname="Aladev", name="Roman", phone=-1, age=0),
            AddUserRequest(surname="Aladev", name="Roman", phone=0, age=0),
        ],
        ids=[
            "Bool",
            "Negative number",
            "0",
        ],
    )
    @allure.title("Check validation for phone field (negative)")
    def test_phone_validation_negative(self, client, user):
        with allure.step("Send Add User request"):
            add_user_req = user
            response = client.send_request(add_user_req)

        with allure.step("Check operation failed"):
            assert (
                response.status == constants.FAILURE_STATUS
            ), f"Status is Successful, {response}"
            assert (
                response.method == constants.ADD_METHOD
            ), f"Response Method is different from Request Method, {response}"
            assert response.reason is not None

    @pytest.mark.parametrize(
        "param",
        [" ", None],
        ids=[
            "No phone field",
            "phone field is Null",
        ],
    )
    @allure.title("Check validation for phone field (negative)")
    def test_phone_validation_negative_raw_request(self, client, param):
        with allure.step("Send Add User request"):
            msg = {
                "method": "add",
                "id": "960d46a3-4b51-11ef-8600-e86a64efce12",
                "name": "Roman",
                "surname": "Aladev",
                "age": 1,
            }

            if param is not None:
                msg["phone"] = None

            client.send_raw_msg(msg)
            resp_json = client.recv_msg()
            response = Response.from_dict(resp_json)

        with allure.step("Check operation failed"):
            assert (
                response.status == constants.FAILURE_STATUS
            ), f"Status is Successful, {response}"
            assert (
                response.method == constants.ADD_METHOD
            ), f"Response Method is different from Request Method, {response}"
            assert response.reason is not None

    @pytest.mark.parametrize(
        "user",
        [
            AddUserRequest(surname="Aladev", name="Roman", phone="1", age=-1),
            AddUserRequest(surname="Aladev", name="Roman", phone="1", age=0),
            AddUserRequest(surname="Aladev", name="Roman", phone="1", age=1),
            AddUserRequest(surname="Aladev", name="Roman", phone="1", age=True),
            pytest.param(
                AddUserRequest(
                    surname="Aladev", name="Roman", phone="1", age=4294967297
                ),
                marks=pytest.mark.skip(
                    reason="Overflow of unsigned int64 for age field"
                ),
            ),
        ],
        ids=["Negative", "0", "Positive", "Bool", "> int32, >int64, >unsigned int"],
    )
    @allure.title("Check validation for age field (positive)")
    def test_age_validation_positive(self, client, user):
        with allure.step("Send Add User request"):
            add_user_req = user
            response = client.send_request(add_user_req)

        with allure.step("Check operation succeed"):
            assert (
                response.status == constants.SUCCESS_STATUS
            ), f"Status is not Successful, {response}"
            assert (
                response.method == constants.ADD_METHOD
            ), f"Response Method is different from Request Method, {response}"

        with allure.step("Perform select using user's phone number"):
            search_user_req = SelectUserRequest(phone=add_user_req.phone)
            response = client.send_request(search_user_req)

        # Note: It is better to query db directly to check such data
        with allure.step("Check user found and all fields filled correctly"):
            assert len(response.users) == 1, f"User not found, {response}"
            response_user = User.from_dict(response.users[0])
            assert_users_equal(response_user, add_user_req)

    @pytest.mark.parametrize(
        "user",
        [
            pytest.param(
                AddUserRequest(
                    surname="Aladev", name="Roman", phone="1", age=3.1
                ),
                marks=pytest.mark.skip(
                    reason="float age is truncated to 3"
                ),
            ),
            pytest.param(
                AddUserRequest(
                    surname="Aladev", name="Roman", phone="1", age=0.1
                ),
                marks=pytest.mark.skip(
                    reason="float age is truncated to 0"
                ),
            ),
            AddUserRequest(surname="Aladev", name="Roman", phone="1", age="1.2A"),
        ],
        ids=[
            "Float",
            "Small float",
            "String",
        ],
    )
    @allure.title("Check validation for age field (negative)")
    def test_age_validation_negative(self, client, user):
        with allure.step("Send Add User request"):
            add_user_req = user
            response = client.send_request(add_user_req)

        with allure.step("Check operation failed"):
            assert (
                response.status == constants.FAILURE_STATUS
            ), f"Status is Successful, {response}"
            assert (
                response.method == constants.ADD_METHOD
            ), f"Response Method is different from Request Method, {response}"
            assert response.reason is not None

    @pytest.mark.parametrize(
        "param",
        [" ", None],
        ids=[
            "No age field",
            "age field is Null",
        ],
    )
    @allure.title("Check validation for age field (negative)")
    def test_age_validation_negative_raw_request(self, client, param):
        with allure.step("Send Add User request"):
            msg = {
                "method": "add",
                "id": "960d46a3-4b51-11ef-8600-e86a64efce12",
                "name": "Roman",
                "surname": "Aladev",
                "phone": "13",
            }

            if param is not None:
                msg["age"] = None

            client.send_raw_msg(msg)
            resp_json = client.recv_msg()
            response = Response.from_dict(resp_json)

        with allure.step("Check operation failed"):
            assert (
                response.status == constants.FAILURE_STATUS
            ), f"Status is Successful, {response}"
            assert (
                response.method == constants.ADD_METHOD
            ), f"Response Method is different from Request Method, {response}"
            assert response.reason is not None
