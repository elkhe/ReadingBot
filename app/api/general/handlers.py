import ast
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message

from app.tg_bot import bot
from app.models import dto
from app.api.general.service import GeneralService
from app.api.general.dao import GeneralImpl
from app.database.pg_client import PgClient 
from app.api.active_list.handlers import get_menu

general = GeneralService(GeneralImpl(PgClient()))


@bot.message_handler(commands=['start'])
def start(message: Message):
    general.start(
        dto.User(
            user_id=message.from_user.id,
            username=message.from_user.username
        )
    )
    bot.send_message(message.chat.id, "Вы зарегистрированы")


@bot.message_handler(commands=['choose_book_for_reading'])
def choose_book_menu(message: Message):
    reply_markup = get_menu(
        dto.User(
            user_id=message.from_user.id,
            username=message.from_user.username
        ),
        callback_prefix='c')
    bot.send_message(
        message.chat.id, 
        "Выберите книгу для чтения из вашего активного списка", 
        reply_markup=reply_markup
    )


@bot.callback_query_handler(func = lambda call: call.data.startswith('["c'))
def choose_book(call: CallbackQuery) -> None:
    callback_data = ast.literal_eval(call.data)
    general.choose_book(
        dto.User(
            user_id=call.from_user.id,
            username=call.from_user.username
        ),
        dto.Book(
            bookname=callback_data[1],
            author=callback_data[2]
        )
    )
    bot.send_message(
        call.message.chat.id,
        f"Книга \"{callback_data[1]}\" {callback_data[2]} успешно выбрана"
    )


@bot.message_handler(commands=["active_book"])
def get_active_book(message: Message):
    book = general.get_active_book(
        dto.User(
            user_id=message.from_user.id,
            username=message.from_user.username
        )
    )
    if book:
        bot.send_message(
            message.chat.id, 
            f"Активная книга: \"{book.bookname}\" {book.author}"
        )
    else:
        bot.send_message(
            message.chat.id, 
            "Сейчас ни одна книга не активна"
        )




