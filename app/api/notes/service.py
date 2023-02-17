from app.api.base.service import BaseService
from app.api.notes.interface import NotesInterface
from app.models import dto
from app.models.models import Note
from typing import List, Tuple


class NotesService(BaseService):
    def __init__(self, notes_dao: NotesInterface) -> None:
        super().__init__(notes_dao)
        self.notes_impl = self.dao

    def get_last_note(self, user_id: int, book_id: int) -> Note | None:
        last_note = self.notes_impl.get_last_note(user_id, book_id)
        return last_note

    def create_note(self, noteDto: dto.Note, bookDto: dto.Book) -> None:
        book = self.get_book(bookDto)
        last_note = self.get_last_note(noteDto.user_id, book.book_id)
        note_number = last_note.number if last_note else 1
        self.notes_impl.create_note(noteDto, note_number, book.book_id)

    def get_note_by_title(self, user_id: int, title: str) -> Note | None:
        note = self.notes_impl.get_note_by_title(user_id, title)
        return note 
    
    def get_all_notes(self, userDto: dto.User) -> Tuple[Note] | None:
        notes = self.notes_impl.get_all_notes(userDto)
        return notes
    
    def get_notes_by_date(self, userDto, date) -> Tuple[Note] | None:
        notes = self.notes_impl.get_notes_by_date(userDto, date)
        return notes
