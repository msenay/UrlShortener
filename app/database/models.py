from sqlalchemy import Column, String, Integer
from app.database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, unique=True, index=True)
    short_url = Column(String, unique=True, index=True)
