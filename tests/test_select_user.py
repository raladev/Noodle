import allure
import pytest

from models import constants
from models.requests import SelectUserRequest


class TestSelectUser:
    @allure.title("Select created user by phone number")
    @pytest.mark.skip(
        reason="status field  contains failed status instead of success when search is successful"
    )
    def test_select_created_user_by_phone(self, client, user):
        with allure.step("Perform select request"):
            user = SelectUserRequest(phone=user.phone)
            response = client.send_request(user)

        with allure.step(
            "Check request if successful and response contains the account"
        ):
            assert (
                response.status == constants.SUCCESS_STATUS
            ), f"Status is not Successful, {response}"
            assert (
                response.method == constants.SELECT_METHOD
            ), f"Response Method is different from Request Method, {response}"
            assert len(response.users) == 1

    @allure.title("Select created user by phone number")
    @pytest.mark.skip(reason="response does not contain users field when no matches in search")
    def test_select_non_existing_user(self, client):
        with allure.step("Perform select request"):
            user = SelectUserRequest(phone="5")
            response = client.send_request(user)

        assert (
            response.status == constants.SUCCESS_STATUS
        ), f"Status is not Successful, {response}"
        assert (
            response.method == constants.SELECT_METHOD
        ), f"Response Method is different from Request Method, {response}"
        assert len(response.users) == 0
