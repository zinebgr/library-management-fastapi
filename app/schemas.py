from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    username:str
    email:str
    
class UserResponse(BaseModel):
    id:int
    username:str
    email:str

    class Config:
        from_attributes = True

class AuthorCreate(BaseModel):
    name:str
    
class AuthorResponse(BaseModel):
    id:int
    name:str

    class Config:
        from_attributes = True

class BookCreate(BaseModel):
    title: str
    genre: str | None = None
    author_id: int
    isbn: str
    available_copies: int=0
    
class BookResponse(BaseModel):
    id:int
    title: str
    genre: str
    author_id: int
    isbn: str
    available_copies: int

    class Config:
        from_attributes = True

class BorrowRecordCreate(BaseModel):
    user_id: int
    book_id: int
    
    
class BorrowRecordResponse(BaseModel):
    id:int
    user_id: int
    book_id: int
    borrow_date: datetime
    return_date: datetime | None = None

    class Config:
        from_attributes = True

