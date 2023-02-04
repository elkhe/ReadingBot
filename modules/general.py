from datetime import datetime
from typing import List, Dict
from telebot.types import Message
from modules import sql_commands
from database.client import db


def get_user(user_id: str):
    user = db.execute_select_command(sql_commands.GET_USER, (user_id, ))
    return user[0] if user else user


def create_user(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    chat_id = message.chat.id
    book_id = None
    last_visit = datetime.now()
    db.execute_command(sql_commands.CREATE_USER, (user_id, username, chat_id, book_id, last_visit))


def get_book(bookname, author):
    book = db.execute_select_command(sql_commands.GET_BOOK_FROM_BOOKS, (bookname, author))
    return book[0] if book else book


def create_book(bookname: str, author: str):
    bookname = bookname.strip()
    author = author.strip()
    db.execute_command(sql_commands.CREATE_BOOK, (bookname, author))

def choose_book(data, user_id):
    bookname = data.split('"')[1].strip()
    author = data.split('"')[2].strip()
    book_id = get_book(bookname, author)[0]
    db.execute_command(sql_commands.UPDATE_ACTIVE_BOOK, (book_id, user_id))



