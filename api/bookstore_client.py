from api.base_client import BaseClient


class BookStoreClient(BaseClient):
    def list_books(self):
        return self.request("GET", "/BookStore/v1/Books")

    def add_books(self, user_id: str, isbns: list[str], token: str):
        payload = {
            "userId": user_id,
            "collectionOfIsbns": [{"isbn": isbn} for isbn in isbns],
        }
        return self.request("POST", "/BookStore/v1/Books", token=token, json=payload)
