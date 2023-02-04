from modules import general
from modules import sql_commands
from database.client import db
from telebot.types import Message
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_book(bookname, author):
    book = general.get_book(bookname, author)
    if book:
        book_id = book[0]
        book_in_active_list = db.execute_select_command(sql_commands.GET_BOOK_FROM_ACTIVE_LIST, (book_id, ))
        return book_id if book_in_active_list else None
    return
    


def add_book(message: Message, book):
    book_id = book[0]
    db.execute_command(sql_commands.ADD_BOOK_TO_ACTIVE_LIST, 
                    (str(book_id), message.from_user.id, datetime.now()))
    db.execute_command(sql_commands.UPDATE_ACTIVE_BOOK, 
                    (str(book_id), message.from_user.id))


def get_list(user_id):
    books = db.execute_select_command(sql_commands.GET_ACTIVE_LIST, (user_id, ))
    return books


def delete_book(data: str):
    bookname = data.split('"')[1].strip()
    author = data.split('"')[2].strip()
    book = general.get_book(bookname, author)
    book_id = book[0]
    db.execute_command(sql_commands.DELETE_FROM_ALIST, (book_id, ))
    

def get_menu(user_id, callback_prefix):
    books = get_list(user_id)
    keyboard = []
    for book in books:
        bookname = f"\"{book[0]}\" {book[1]}\n"
        callback_data = f"{callback_prefix}{bookname}"
        keyboard.append([InlineKeyboardButton(bookname, callback_data=callback_data)])
    return InlineKeyboardMarkup(keyboard)

