from urllib.parse import quote_plus

from sqlalchemy import BIGINT, Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from settings import SQLALCHEMY_DATABASE_URL


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class InstaQuery(Base):
    __tablename__ = "insta_query"

    id = Column(Integer, primary_key=True)
    url = Column(Text)
    parse_url = Column(Text)
    status = Column(String(length=10))
    created_at = Column(BIGINT)



def create_item(db: Session, data):
    db_item = InstaQuery(**data)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

