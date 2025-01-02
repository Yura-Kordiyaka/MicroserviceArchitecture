from db.conf.session import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import DateTime, func


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    confirm_email = Column(Boolean, default=False)
    created_at = mapped_column(DateTime, default=func.now())
    updated_at = mapped_column(DateTime, default=func.now(), onupdate=func.now())
