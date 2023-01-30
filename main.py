import telebot
from telebot.types import Message
from datetime import date, datetime

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
    user_id = message.from_user.id
    username = message.from_user.username
    chat_id = message.chat.id
    create_new_user = False
    user = bot.database.get_user(user_id=str(user_id))
    if not user:
        bot.database.create_user(
                                user_id=str(user_id), 
                                username=username, 
                                chat_id=str(chat_id), 
                                state=False, 
                                last_visit=datetime.now())
        create_new_user = True
    bot.reply_to(message=message, text=f"Вы {'уже ' if not create_new_user else ' '}зарегистрированы,  {username}!")

@bot.message_handler(commands=['add_book_to_active_list'])
def add_to_active_list(message: Message):
    """
    Get bookname. Get author. Check bookname in active_list. Add to active list if absent.
    Check bookname in books. Add to books if absent. 
    """
    bot.send_message(chat_id=message.chat.id, text="Введите название книги")
    bot.register_next_step_handler(message, get_bookname)

def get_bookname(message: Message):
    bot.send_message(chat_id=message.chat.id, text="Введите имя автора")
    bot.register_next_step_handler(message, add_data_to_active_list, bookname=message.text)

def add_data_to_active_list(message: Message, bookname):
    author = message.text
    book = bot.database.get_book(bookname, author)
    print(book)
    if book:
        book_id = book[0]
        book_in_al = bot.database.get_book_from_alist(book_id=book_id)
        if book_in_al:
            bot.send_message(chat_id=message.chat.id, text='Эта книга уже есть в вашем активном списке')
        else:
            bot.database.add_book_to_alist(
                                            started_reading=datetime.now(),
                                            user_id=message.from_user.id,
                                            book_id=book_id)
            bot.send_message(chat_id=message.chat.id, text='Книга добавлена в ваш активный список')
    else:
        bot.database.create_book(book_name=bookname, author_name=author)
        book_id = bot.database.get_book(bookname, author)
        bot.database.add_book_to_alist(
                                started_reading=datetime.now(),
                                user_id=message.from_user.id,
                                book_id=book_id)
        bot.send_message(chat_id=message.chat.id, text='Книга создана и добавлена в ваш активный список')







    







#while True:
try:
    bot.setup_resources()
    bot.polling()
except Exception as err:
    print(f"{err.__class__} ::: {err}")
    bot.tg_client.post(method="sendMessage", params={"text": err,
                                                    "chat_id": ADMIN_CHAT_ID})

