import uuid
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum as SQLAlchemyEnum,
    JSON
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.mysql import CHAR
import enum
from datetime import datetime

Base = declarative_base()

class DeckCategory(enum.Enum):
    HARDWARE_OS = "Hardware & Betriebssysteme"
    NETWORKING = "Vernetzte Systeme"
    APP_DEV = "Anwendungsentwicklung"
    BUSINESS_SOCIAL = "Wirtschafts- & Sozialkunde"

class User(Base):
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    total_xp = Column(Integer, default=0)
    current_level = Column(Integer, default=1)

    progress = relationship("UserProgress", back_populates="user")

class Deck(Base):
    __tablename__ = "decks"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    category = Column(SQLAlchemyEnum(DeckCategory), nullable=False)

    cards = relationship("Card", back_populates="deck")

class Card(Base):
    __tablename__ = "cards"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    deck_id = Column(CHAR(36), ForeignKey("decks.id"), nullable=False)
    front = Column(JSON, nullable=False)
    back = Column(JSON, nullable=False)
    base_difficulty = Column(Integer, default=1)

    deck = relationship("Deck", back_populates="cards")
    progress = relationship("UserProgress", back_populates="card")

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    card_id = Column(CHAR(36), ForeignKey("cards.id"), nullable=False)
    current_box = Column(Integer, default=1)
    next_review = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="progress")
    card = relationship("Card", back_populates="progress")

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    criteria = Column(JSON)
    icon_url = Column(String(255))

class BossFightSession(Base):
    __tablename__ = "boss_fight_sessions"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False, unique=True) # A user can only have one active session
    boss_hp = Column(Integer, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
