from typing import List
from datetime import datetime
from sqlalchemy import ForeignKey, String, Date, DateTime, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin

# Declare base for metadata
class Base(DeclarativeBase):
    pass

# Create user_acocunt table
class User(UserMixin, Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String(50))
    first_name: Mapped[str] = mapped_column(String(50))
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    esr_number: Mapped[int] = mapped_column(Integer(), unique=True, nullable=False)
    password_hash: Mapped[str]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, esr_number={self.esr_number!r})"

# Create address table
class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email={self.email!r})"

def create_tables(engine):
    Base.metadata.create_all(engine) 
