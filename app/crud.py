from datetime import datetime ,timezone
from sqlalchemy import Select
from sqlalchemy.orm import Session
from app.models import User, Book, Author, BorrowRecord

class UserNotFoundError(Exception):
    pass

class BookNotFoundError(Exception):
    pass

class NoAvailableCopiesError(Exception):
    pass

class BorrowRecordNotFoundError(Exception):
    pass

class BorrowRecordAlreadyReturnedError(Exception):
    pass

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, username: str, email: str):
    exist = db.query(User).filter(User.email == email).first()
    if exist:
        return None
    db_user = User(username=username, email=email)    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def get_books(db: Session):
    return db.query(Book).all()

def create_book(db: Session, title: str, genre: str, author_id: int, isbn: str, available_copies: int):
    exist = db.query(Book).filter(Book.isbn == isbn).first()
    if exist:
        return None
    db_book = Book(title=title, genre=genre, author_id=author_id, isbn=isbn, available_copies=available_copies)    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book_copies(db: Session, book_id: int, new_copies: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return None
    book.available_copies = new_copies
    db.commit()
    db.refresh(book)
    return book

def get_author(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()

def get_authors(db: Session):
    return db.query(Author).all()

def create_author(db: Session,name: str):
    db_author = Author(name=name)    
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_br_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    return db.query(BorrowRecord).filter(BorrowRecord.user_id == user_id).all()

def get_act_br(db: Session):
    return db.query(BorrowRecord).filter(BorrowRecord.return_date == None).all()

def borrow_book(db: Session, user_id: int, book_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundError(f"User {user_id} not found")
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise BookNotFoundError(f"Book with id {book_id} not found")
    if book.available_copies <= 0:
        raise NoAvailableCopiesError(f"Book '{book.title}' has no available copies")
    book.available_copies -= 1
    new_borrow = BorrowRecord(
        user_id=user_id,
        book_id=book_id,
        borrow_date=datetime.now(timezone.utc),
        return_date=None
    )
    db.add(new_borrow)
    db.commit()
    db.refresh(new_borrow)
    return new_borrow

def return_book(db: Session, br_id: int):
    borrow = db.query(BorrowRecord).filter(BorrowRecord.id == br_id).first()
    if not borrow:
        raise BorrowRecordNotFoundError(f"Borrow record {br_id} not found")
    if borrow.return_date is not None:
        raise BorrowRecordAlreadyReturnedError(f"Borrow record {br_id} already returned")
    book = db.query(Book).filter(Book.id == borrow.book_id).first()
    if book:
        book.available_copies += 1
    borrow.return_date = datetime.now(timezone.utc)
    db.commit()
    db.refresh(borrow)
    return borrow

