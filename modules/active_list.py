from modules import general
from modules import sql_commands
from database.client import db
from telebot.types import Message
from datetime import datetime

def get_book(bookname, author):
    book = general.get_book(bookname, author)
    if book:
        book_id = book[0]
        book_in_active_list = db.execute_select_command(sql_commands.GET_BOOK_FROM_ACTIVE_LIST, (book_id, ))
    return book_id if book else None


def add_book(message: Message, book):
    book_id = book[0]
    db.execute_command(sql_commands.ADD_BOOK_TO_ACTIVE_LIST, 
                    (str(book_id), message.from_user.id, datetime.now()))


def get_list(user_id):
    books = db.execute_select_command(sql_commands.GET_ACTIVE_LIST, (user_id, ))
    return books

