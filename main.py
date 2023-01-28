import telebot
from telebot.types import Message
from datetime import date

from database.client import PgClient
from database.db_config import host, db_name, password, user
from database.actions import Database

from telegram.config import TOKEN, ADMIN_CHAT_ID, BASE_URL
from telegram.client import TelegramClient



class ReadingBot(telebot.TeleBot):
    def __init__(self, tg_client: TelegramClient, database: PgClient, *args, **kwargs ):
        super().__init__(*args, **kwargs)
        self.tg_client = tg_client
        self.database = database
    
    def setup_resources(self):
        self.database.setup()


tg_client = TelegramClient(TOKEN, BASE_URL)
database = Database(PgClient(host, db_name, password, user))

bot = ReadingBot(token=TOKEN, tg_client=tg_client, database=database)


@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, str(chat_id))



#while True:
try:
    bot.setup_resources()
    bot.polling()
except Exception as err:
    print(f"{err.__class__} ::: {err}")
    bot.tg_client.post(method="sendMessage", params={"text": err,
                                                    "chat_id": ADMIN_CHAT_ID})

