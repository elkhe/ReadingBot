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
    bot.send_message(message.chat.id, _prepare_active_list_msg(active_list_books))


def _get_book_msg(book: tuple):
    return f"\"{book[0]}\" {book[1]}\n" if book else book


def _prepare_active_list_msg(books):
    msg = "Список читаемых книг:\n\n" + "\n".join([_get_book_msg(book) for book in books])
    return msg


#alter table users with del on cascade or smth for users.book_id
@bot.message_handler(commands=['delete_book_from_active_list'])
def get_book_for_delete(message: Message):
    reply_markup = active_list.get_menu(message.from_user.id, callback_prefix='d')        
    bot.send_message(message.chat.id, "Выберите книгу для удаления", reply_markup=reply_markup)


@bot.callback_query_handler(func = lambda call: call.data.startswith("d"))
def delete_book_from_active_list(call):
    active_list.delete_book(call.data)
    text = call.data.strip("\n")
    text = call.data.lstrip("d")
    bot.send_message(call.message.chat.id, f"Книга {text} удалена")
    get_active_list(call.message)


@bot.message_handler(commands=['choose_book_for_reading'])
def choose_book_menu(message: Message):
    reply_markup = active_list.get_menu(message.from_user.id, callback_prefix='c')
    bot.send_message(message.chat.id, "Выберите книгу для чтения из вашего активного списка", reply_markup=reply_markup)


@bot.callback_query_handler(func = lambda call: call.data.startswith("c"))
def choose_book(call):
    general.choose_book(call.data, call.message.from_user.id)
    bot.send_message(call.message.chat.id, f"Книга {call.data} успешно выбрана")





#while True:
try:
    bot.polling()
except Exception as err:
    print(f"{err.__class__} ::: {err}")


