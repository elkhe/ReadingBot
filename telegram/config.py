import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')
BASE_URL = "https://api/telegram/"