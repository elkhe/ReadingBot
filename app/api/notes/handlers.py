import ast
from datetime import datetime
from app.api.notes.service import NotesService
from app.api.notes.dao import NotesImpl
from app.database.pg_client import PgClient
from app.api.active_list import handlers as active_list
from app.tg_bot import bot
from app.models.models import Note
from app.models import dto
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message


notes = NotesService(NotesImpl(PgClient()))


@bot.message_handler(commands=['create_note'])
def create_note_menu(message: Message):
    active_book = notes.get_active_book(
        dto.User(
            user_id=message.from_user.id, 
            username=message.from_user.username
        )
    )
    if active_book:
        affirm_button = InlineKeyboardButton(
            "Да", 
            callback_data="['note', 'yes', '" + active_book.bookname + "', '" + active_book.author + "']"
        )
        change_button = InlineKeyboardButton(
            "Выбрать другую книгу", 
            callback_data="['note', 'change']"
        )
        reply_markup = InlineKeyboardMarkup([[affirm_button], [change_button]])
        bot.send_message(
            message.chat.id, 
            f"Создать заметку по книге {_get_book_msg(active_book)}?", 
            reply_markup=reply_markup
        )

def _get_book_msg(book: dto.Book):
    return f"\"{book.bookname}\" {book.author}\n" if book else "-"

@bot.callback_query_handler(func = lambda call: call.data.startswith("['note"))
def create_note_choice(call: CallbackQuery):
    callback_data = ast.literal_eval(call.data)
    if callback_data[1] == "yes":
        bot.send_message(call.from_user.id, text="Введите название заметки")
        bot.register_next_step_handler(
            call.message, 
            get_note_data, 
            bookDto=dto.Book(
                bookname=callback_data[2], 
                author=callback_data[3])
        )
    elif callback_data[1] == "change":
        reply_markup = active_list.get_menu(
            dto.User(
                user_id=call.from_user.id,
                username=call.from_user.username
            ), 
            callback_prefix='c'
        )
        bot.send_message(
            call.from_user.id, 
            "Выберите книгу для чтения из вашего активного списка", 
            reply_markup=reply_markup
        )
        

def get_note_data(message: Message, bookDto: dto.Book):
    bot.send_message(message.chat.id, "Введите текст заметки")
    bot.register_next_step_handler(message, create_note, bookDto, message.text)


def create_note(message: Message, bookDto: dto.Book, title:str):
    date = datetime.now()
    notes.create_note(
        dto.Note(
            title=title,            
            text=message.text,
            date=date,
            user_id=message.from_user.id,
            book_id=None
        ),
        bookDto=bookDto

    )
    bot.send_message(message.chat.id, f"Заметка создана")


@bot.message_handler(commands=['get_note'])
def get_note_menu(message: Message):
    active_book = notes.get_active_book(
        dto.User(
            user_id=message.from_user.id,
            username=message.from_user.username
        )
    )
    title_button = InlineKeyboardButton(
        "Название", 
         callback_data="['getnote', 'title']"
    )
    data_button = InlineKeyboardButton(
        "Дата", 
        callback_data="['getnote', 'date']"
    )
    whole_button = InlineKeyboardButton(
        "Все", 
        callback_data="['getnote', 'all']"
    )
    keyboard = [[title_button], [data_button], [whole_button]]
    reply_markup = InlineKeyboardMarkup(keyboard=keyboard)
    bot.send_message(
        message.chat.id, 
        f"Выберите критерий поиска для книги{_get_book_msg(active_book)}", 
        reply_markup=reply_markup
    )


@bot.callback_query_handler(func = lambda call: call.data.startswith("['getnote"))
def create_note_choice(call: CallbackQuery):
    callback_data = ast.literal_eval(call.data)
    if callback_data[1] == "title":
        bot.send_message(call.message.chat.id, text="Введите название заметки")
        bot.register_next_step_handler(call.message, get_note_by_title)
    elif callback_data[1] == "date":
        bot.send_message(call.message.chat.id, text="Введите дату в формате ДД-ММ-ГГ")
        bot.register_next_step_handler(call.message, get_notes_by_date)
    elif callback_data[1] == "all":
        get_all_notes(call)

def get_note_by_title(message: Message):
    note = notes.get_note_by_title(
        user_id=message.from_user.id,
        title=message.text
    )
    if note:
        bot.send_message(message.chat.id, text=_create_note_msg(note))
    else:
        print("Такой заметки нет")

def _create_note_msg(note: Note) -> str:
    msg = (
        f"Название заметки: {note.title}\n\n\n"
        f"Текст:\n{note.text}\n\n\n"
        f"Дата создания: {note.date.strftime('%d %B, %Y')}\n"
        f"Номер заметки: {note.number}"
        
    )
    return msg


def get_notes_by_date(message: Message):
    try:
        date = datetime.strptime(message.text, '%d-%m-%y')
    except ValueError as ve:
        print('Value error:', ve)
    notes_by_date = notes.get_notes_by_date(
            dto.User(
                user_id=message.from_user.id,
                username=message.from_user.username
            ),
            date
        )
    if notes_by_date:
        for note in notes_by_date:
            bot.send_message(
                message.chat.id, 
                text=_create_note_msg(note)
            )
    else:
        bot.send_message(message.chat.id, text="Заметок за этот день нет")       
    

def get_all_notes(call: CallbackQuery):
    all_notes = notes.get_all_notes(
        dto.User(
            user_id=call.from_user.id,
            username=call.from_user.username
        )
    )
    if all_notes:
        for note in all_notes:
            bot.send_message(
                call.message.chat.id, 
                _create_note_msg(note)
            )
    else: 
        bot.send_message(
            call.message.chat.id,
            "По этой книге у вас нет заметок"
        )
    