
import pytest

from helpers.utils import assert_users_equal
from models import constants
from models.requests import AddUserRequest, SelectUserRequest, DeleteUserRequest
import allure

from models.responses import User, Response


class TestAddUserUseCases:

    @allure.title("Add first user and check it is exists using select")
    def test_add_first_user(self, client):
        with allure.step("Send Add User request"):
            add_user_req = AddUserRequest(
                name="Roman", surname="Aladev", phone="8913", age=15
            )
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
        "second_user",
        [
            AddUserRequest(name="Roman", surname="Aladev1", phone="1", age=151),
            AddUserRequest(name="R", surname="Aladev", phone="2", age=0),
            AddUserRequest(name="Roman2", surname="Aladev2", phone="3", age=15),
            AddUserRequest(name="Roman", surname="Aladev", phone="4", age=15),
        ],
        ids=[
            "User with same name",
            "User with same surname",
            "User with same age",
            "User with same all same fields except phone",
        ],
    )
    @allure.title("Add several users")
    def test_add_several_users(self, client, second_user):
        with allure.step("Add first user"):
            first_user = AddUserRequest(
                name="Roman", surname="Aladev", phone="5", age=15
            )
            response = client.send_request(first_user)
            assert (
                response.status == constants.SUCCESS_STATUS
            ), f"Status is not Successful, {response}"

        with allure.step("Add second user"):
            response = client.send_request(second_user)
            assert (
                response.status == constants.SUCCESS_STATUS
            ), f"Status is not Successful, {response}"
            assert (
                response.method == constants.ADD_METHOD
            ), f"Response Method is different from Request Method, {response}"

        with allure.step("Perform select using second user's phone number"):
            search_user_req = SelectUserRequest(phone=second_user.phone)
            response = client.send_request(search_user_req)

        with allure.step("Check user found and all fields filled correctly"):
            assert len(response.users) == 1, f"User not found, {response}"
            response_user = User.from_dict(response.users[0])
            assert_users_equal(response_user, second_user)

        with allure.step("Check data of first user is not changed"):
            search_user_req = SelectUserRequest(phone=first_user.phone)
            response = client.send_request(search_user_req)
            assert len(response.users) == 1, f"User not found, {response}"
            response_user = User.from_dict(response.users[0])
            assert_users_equal(response_user, first_user)

    @allure.title("Add user with existing phone number")
    @pytest.mark.skip(
        reason="Failure message for duplicate user creation case does not contain reason of failure (reason field is missing)"
    )
    def test_add_user_with_existing_phone(self, client):
        first_user = AddUserRequest(name="Roman", surname="Aladev", phone="5", age=15)
        second_user = AddUserRequest(name="R", surname="A", phone="5", age=10)

        with allure.step("Add first user"):
            response = client.send_request(first_user)
            assert (
                response.status == constants.SUCCESS_STATUS
            ), f"Status is not Successful, {response}"

        with allure.step("Add second user"):
            response = client.send_request(second_user)
            assert (
                response.status == constants.FAILURE_STATUS
            ), f"Status is not Failure, {response}"
            assert (
                response.method == constants.ADD_METHOD
            ), f"Response Method is different from Request Method, {response}"
            assert response.reason is not None

        with allure.step("Perform select using  phone number"):
            search_user_req = SelectUserRequest(phone=second_user.phone)
            response = client.send_request(search_user_req)

        with allure.step("Check only one user found and all fields filled correctly"):
            assert len(response.users) == 1, f"User found, {response}"
            response_user = User.from_dict(response.users[0])
            assert_users_equal(response_user, first_user)

    @allure.title("Add deleted user")
    def test_add_deleted_user(self, client):
        user = AddUserRequest(name="Roman", surname="Aladev", phone="5", age=15)
        recreated_user = AddUserRequest(name="R", surname="A", phone="5", age=10)

        with allure.step("Add user"):
            response = client.send_request(user)
            assert (
                response.status == constants.SUCCESS_STATUS
            ), f"Status is not Successful, {response}"

        with allure.step("Delete user"):
            req = DeleteUserRequest(phone=user.phone)
            response = client.send_request(req)
            assert (
                response.status == constants.SUCCESS_STATUS
            ), f"Status is not Successful, {response}"

        with allure.step("Check user deleted using search"):
            search_user_req = SelectUserRequest(phone=user.phone)
            response = client.send_request(search_user_req)
            assert response.users == None, f"User found, {response}"

        with allure.step("Add user with same number, but different name/surname/age"):
            response = client.send_request(recreated_user)
            assert (
                response.status == constants.SUCCESS_STATUS
            ), f"Status is not Successful, {response}"

        with allure.step("Check user exists and has updated data"):
            search_user_req = SelectUserRequest(phone=recreated_user.phone)
            response = client.send_request(search_user_req)
            assert len(response.users) == 1, f"User not found, {response}"
            response_user = User.from_dict(response.users[0])
            assert_users_equal(response_user, recreated_user)