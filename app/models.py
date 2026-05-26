from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.orm import declarative_base
# from settings import setting as st

Base = declarative_base()

class BorrowRecord (Base):
    __tablename__ = "borrowrecords"
    id = Column(Integer, primary_key=True)
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, default=None, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    genre = Column(String(50), nullable=True)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE", onupdate="CASCADE"))
    isbn = Column(String(13), unique=True, nullable=False)
    available_copies = Column(Integer, default=0)
    users = relationship('User', secondary='borrowrecords', back_populates='books')
    author = relationship("Author", back_populates="books")

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    books = relationship("Book", back_populates="author", cascade="all, delete, save-update")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False, index=True)
    books = relationship('Book', secondary='borrowrecords', back_populates='users')
