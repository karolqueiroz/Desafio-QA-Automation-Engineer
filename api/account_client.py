from api.base_client import BaseClient


class AccountClient(BaseClient):
    def create_user(self, user_name: str, password: str):
        return self.request(
            "POST", "/Account/v1/User",
            json={"userName": user_name, "password": password},
        )

    def generate_token(self, user_name: str, password: str):
        return self.request(
            "POST", "/Account/v1/GenerateToken",
            json={"userName": user_name, "password": password},
        )

    def is_authorized(self, user_name: str, password: str):
        return self.request(
            "POST", "/Account/v1/Authorized",
            json={"userName": user_name, "password": password},
        )

    def get_user(self, user_id: str, token: str):
        return self.request("GET", f"/Account/v1/User/{user_id}", token=token)
