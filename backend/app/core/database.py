from app.core.config import DATABASE_URL

from sqlmodel import Session, create_engine

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300
)

def get_session():
    with Session(engine) as session:
        yield session