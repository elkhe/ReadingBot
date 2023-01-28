import requests
from telegram.config import ADMIN_CHAT_ID, TOKEN, BASE_URL
class TelegramClient:
    def __init__(self, token: str, base_url: str) -> None:
        self.token = token
        self.base_url = base_url
    
    def prepare_url(self, method: str):
        result_url = f"{self.base_url}/bot{self.token}/"
        if method is not None:
            result_url += method
        return result_url

    def post(self, method: 
        str = None, params: dict = None, body: dict = None):
        url = self.prepare_url(method)
        resp = requests.post(url, data=body)

if __name__ == "__main__":
    token = TOKEN
    telegram_client = TelegramClient(token=token, base_url=BASE_URL)
    my_params = {"chat_id": ADMIN_CHAT_ID, "text": "aloha"}
    telegram_client.post(method="sendMessage", params=my_params)

