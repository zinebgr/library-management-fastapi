from sqlalchemy.orm import sessionmaker
from app.settings import setting as st 
from sqlalchemy import create_engine

db_con = f"mysql+pymysql://{st.db_user}:{st.db_pass}@{st.db_host}/{st.db_name}?charset=utf8mb4"
engine = create_engine(db_con, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
