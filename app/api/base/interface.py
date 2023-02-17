from app.models import dto
from datetime import datetime

class BaseInterface:
    def get_book(self, bookDto: dto.Book):
        pass

    def create_book(self, bookDto: dto.Book):
        pass

    def get_user(self, userDto: dto.User):
        pass