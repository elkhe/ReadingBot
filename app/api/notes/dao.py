from app.api.notes.interface import NotesInterface
from app.api.base.dao import BaseImpl
from app.models import dto
from app.models.models import Note
from typing import List, Tuple
from datetime import datetime

class NotesImpl(NotesInterface, BaseImpl):
    def __init__(self, database_client) -> None:
        super().__init__(database_client)

    def get_last_note(self, user_id: int, book_id: int) -> Note | None:
        last_note = self.db.execute_select_command("""
            SELECT note_id, title, note_text, MAX(note_number), note_date, user_id, book_id 
              FROM notes 
             WHERE user_id = %s and book_id = %s
             GROUP BY note_id;
        """,
            (user_id, book_id)
        )
        return Note(*last_note[0]) if last_note else None

    def create_note(self, noteDto: dto.Note, note_number, book_id: int) -> None:
        self.db.execute_command("""
            INSERT INTO notes(note_text, title, note_number, note_date, user_id, book_id)
            VALUES (%s, %s, %s, %s, %s, %s);
        """,
            (
                noteDto.text, 
                noteDto.title, 
                note_number, 
                noteDto.date, 
                noteDto.user_id, 
                book_id
            )
        )

    def get_note_by_title(self, user_id, title) -> Note | None:
        note = self.db.execute_select_command("""
            SELECT note_id, title, note_text, note_number, note_date, notes.user_id, notes.book_id
              FROM notes INNER JOIN users
                ON notes.user_id = users.user_id
               AND notes.book_id = (
                    SELECT users.book_id
                      FROM users
                     WHERE users.user_id = %s)
             WHERE title = %s;
        """,
            (user_id, title)    
        )
        return Note(*note[0]) if note else None
    
    def get_notes_by_date(self, userDto:dto.User, date: datetime) -> Tuple[Note] | None:
        note_rows = self.db.execute_select_command("""
            SELECT note_id, title, note_text, note_number, note_date, notes.user_id, notes.book_id
              FROM notes INNER JOIN users
                ON notes.user_id = users.user_id
               AND notes.book_id = (
                    SELECT users.book_id
                        FROM users
                        WHERE users.user_id = %s)
             WHERE note_date = %s;        
            """,
            (userDto.user_id, date)
        )
        notes = [Note(*note) for note in note_rows]
        return tuple(notes)
    
    def get_all_notes(self, userDto: dto.User) -> Tuple[Note]:
        note_rows = self.db.execute_select_command("""
            SELECT note_id, title, note_text, note_number, note_date, notes.user_id, notes.book_id
              FROM notes INNER JOIN users
                ON notes.user_id = users.user_id
               AND notes.book_id = (
                    SELECT users.book_id
                        FROM users
             WHERE users.user_id = %s)
            """,
            (userDto.user_id, )
        )
        notes = [Note(*note) for note in note_rows]
        return tuple(notes)
    

        