from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db  
from app import crud, schemas  

app = FastAPI()

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.create_user(db, username=user.username, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Failed to create user")
    return db_user

@app.get("/users/", response_model=list[schemas.UserResponse])
def get_users(db:Session=Depends(get_db)):
    return crud.get_users(db)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/authors/", response_model=schemas.AuthorResponse)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db, name=author.name)

@app.get("/authors/", response_model=list[schemas.AuthorResponse])
def get_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db)

@app.get("/authors/{author_id}", response_model=schemas.AuthorResponse)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@app.post("/books/", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.create_book(
        db,
        title=book.title,
        genre=book.genre,
        author_id=book.author_id,
        isbn=book.isbn,
        available_copies=book.available_copies
    )
    if db_book is None:
        raise HTTPException(status_code=400, detail="ISBN already exists or author invalid")
    return db_book

@app.get("/books/", response_model=list[schemas.BookResponse])
def get_books(db: Session = Depends(get_db)):
    return crud.get_books(db)

@app.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}/copies")
def update_copies(book_id: int, new_copies: int, db: Session = Depends(get_db)):
    book = crud.update_book_copies(db, book_id, new_copies)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Copies updated", "available_copies": book.available_copies}

@app.post("/borrow/", response_model=schemas.BorrowRecordResponse)
def borrow_book(record: schemas.BorrowRecordCreate, db: Session = Depends(get_db)):
    try:
        result = crud.borrow_book(db, user_id=record.user_id, book_id=record.book_id)
    except crud.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except crud.BookNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except crud.NoAvailableCopiesError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result

@app.post("/return/{borrow_id}", response_model=schemas.BorrowRecordResponse)
def return_book(borrow_id: int, db: Session = Depends(get_db)):
    try:
        result = crud.return_book(db, borrow_id)
    except crud.BorrowRecordNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except crud.BorrowRecordAlreadyReturnedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result

@app.get("/borrow/user/{user_id}", response_model=list[schemas.BorrowRecordResponse])
def get_user_borrows(user_id: int, db: Session = Depends(get_db)):
    rec = crud.get_br_user(db, user_id)
    if rec is None:
        raise HTTPException(status_code=404, detail="User not found")
    return rec

@app.get("/borrow/active/", response_model=list[schemas.BorrowRecordResponse])
def get_active_borrows(db: Session = Depends(get_db)):
    return crud.get_act_br(db)
