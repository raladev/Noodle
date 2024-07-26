import allure

from models import constants
from models.requests import DeleteUserRequest, SelectUserRequest


class TestDeleteUser:
    @allure.title("Delete created user")
    def test_delete_user(self, client, user):
        with allure.step("Delete user"):
            req = DeleteUserRequest(phone=user.phone)
            response = client.send_request(req)
            assert (
                response.status == constants.SUCCESS_STATUS
            ), f"Status is not Successful, {response}"

        with allure.step("Check user deleted using search"):
            search_user_req = SelectUserRequest(phone=user.phone)
            response = client.send_request(search_user_req)
            assert response.users is None, f"User found, {response}"
