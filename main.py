import os
from dotenv import load_dotenv
import telebot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telebot.util import quick_markup
from datetime import date, datetime

from modules import active_list, general

load_dotenv()

TOKEN = os.getenv('TOKEN')
ADMIN_CHAT_ID = os.getenv('TOKEN')


bot = telebot.TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start(message: Message):
    user = general.get_user(user_id=str(message.from_user.id))
    if not user:
        general.create_user(message)
    bot.send_message(message.chat.id, "Вы зарегистрированы")


@bot.message_handler(commands=['add_book_to_active_list'])
def add_to_active_list(message: Message):
    bot.send_message(chat_id=message.chat.id, text="Введите название книги")
    bot.register_next_step_handler(message, get_bookname)


def get_bookname(message: Message):
    bot.send_message(chat_id=message.chat.id, text="Введите имя автора")
    bot.register_next_step_handler(message, add_book_to_active_list, bookname=message.text)


def add_book_to_active_list(message: Message, bookname):
    author = message.text
    book = active_list.get_book(bookname, author)
    if book:
        bot.send_message(message.chat.id, "Книга уже в активном списке")
        return
    elif not general.get_book(bookname, author):
        general.create_book(bookname, author)
        book = general.get_book(bookname, author)
    active_list.add_book(message, book)
    bot.send_message(message.chat.id, "Книга успешно добавлена в ваш активный список")


@bot.message_handler(commands=['get_active_list'])
def get_active_list(message: Message):
    active_list_books = active_list.get_list(message.from_user.id)
    bot.send_message(message.chat.id, _prepare_active_list(active_list_books))


def _parse_bookname(book: tuple):
    return f"\"{book[0]}\" {book[1]}\n" if book else book


def _prepare_active_list(books):
    msg = "\n".join([_parse_bookname(book) for book in books])
    print(msg)
    return msg


@bot.message_handler(commands=['delete_book_from_active_list'])
def get_book_for_delete(message: Message):
    books = active_list.get_list(message.from_user.id)
    buttons = {_parse_bookname(book):{'callback_data': 'whatever'} for book in books}
    bot.send_message(message.chat.id, text="Выберите книгу для удаления", reply_markup=quick_markup(buttons, row_width=1))
    bot.register_next_step_handler(message, delete_book_from_alist)


def delete_book_from_alist(message: Message):
    pass
    


#while True:
try:
    bot.polling()
except Exception as err:
    print(f"{err.__class__} ::: {err}")


