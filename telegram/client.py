import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TelegramClient:
    def __init__(self) -> None:
        self.token = os.getenv('TOKEN')
        self.base_url = os.getenv('BASE_URL')
    
    def prepare_url(self, method: str):
        result_url = f"{self.base_url}/bot{self.token}/"
        if method is not None:
            result_url += method
        return result_url

    def post(self, method: 
        str = None, params: dict = None, body: dict = None):
        url = self.prepare_url(method)
        resp = requests.post(url, data=body)

#another problem
if __name__ == "__main__":
    TOKEN = os.getenv('TOKEN')
    ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
    BASE_URL = os.getenv('BASE_URL')
    telegram_client = TelegramClient(token=TOKEN, base_url=BASE_URL)
    my_params = {"chat_id": ADMIN_CHAT_ID, "text": "aloha"}
    telegram_client.post(method="sendMessage", params=my_params)

