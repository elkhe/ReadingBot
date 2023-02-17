import ast
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message

from app.tg_bot import bot
from app.models import dto
from app.api.active_list.service import ActiveListService
from app.api.active_list.dao import ActiveListImpl
from app.database.pg_client import PgClient


active_list = ActiveListService(ActiveListImpl(PgClient()))


@bot.message_handler(commands=['add_book_to_active_list'])
def add_to_active_list(message: Message):
    bot.send_message(chat_id=message.chat.id, text="Введите название книги")
    bot.register_next_step_handler(message, get_bookname)


def get_bookname(message: Message):
    bot.send_message(chat_id=message.chat.id, text="Введите имя автора")
    bot.register_next_step_handler(message, add_book_to_active_list, bookname=message.text)


#add and choose book
def add_book_to_active_list(message: Message, bookname):
    author = message.text
    result = active_list.add_book(
        dto.User(
            user_id=message.from_user.id, 
            username=message.from_user.username,
        ), 
        dto.Book(
            bookname=bookname,
            author=author
        ))
    if result:
        bot.send_message(message.chat.id, "Книга успешно добавлена в ваш активный список")
    else:
        bot.send_message(message.chat.id, "Книга уже в активном списке") 


@bot.message_handler(commands=['get_active_list'])
def get_active_list(message: Message):
    result = active_list.get_list(
        dto.User(
            user_id=message.from_user.id, 
            username=message.from_user.username,
        )
    )
    bot.send_message(message.chat.id, _active_list_msg(result))



def _get_book_msg(book: dto.Book):
    return f"\"{book.bookname}\" {book.author}\n" if book else book


def _active_list_msg(active_list: dto.ActiveList):
    msg = (
        f"Список читаемых книг:\n\n" + 
        "\n".join([_get_book_msg(book) for book in active_list.books])
    )
    return msg


#alter table users with del on cascade or smth for users.book_id
@bot.message_handler(commands=['delete_book_from_active_list'])
def get_book_for_delete(message: Message):
    reply_markup = get_menu(
        dto.User(
            user_id=message.from_user.id,
            username=message.from_user.username,
        ), 
        callback_prefix='d')        
    bot.send_message(message.chat.id, "Выберите книгу для удаления", reply_markup=reply_markup)


def get_menu(user: dto.User, callback_prefix) -> InlineKeyboardMarkup:
    books = active_list.get_list(user).books
    keyboard = []
    for book in books:
        button_text = f"\"{book.bookname}\" {book.author}\n"
        callback_data = (
            '["' + callback_prefix + '", \"' 
            + book.bookname + '", \"' 
            + book.author + '"]'
        )
        keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
    return InlineKeyboardMarkup(keyboard)


@bot.callback_query_handler(func = lambda call: call.data.startswith('[\"d"'))
def delete_book_from_active_list(call: CallbackQuery):
    callback_data = ast.literal_eval(call.data)
    active_list.delete_book(
        dto.Book(
            bookname=callback_data[1],
            author=callback_data[2]
        )
    )
    bot.send_message(
        call.message.chat.id, 
        f"Книга \"{callback_data[1]}\" {callback_data[2]} удалена")
    get_active_list(call.message)