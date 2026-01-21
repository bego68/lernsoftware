from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import List, Dict, Any

# Base schema for a card's content (front or back)
class CardContent(BaseModel):
    text: str
    code: str | None = None
    image_url: str | None = None

# Schema for a single card
class Card(BaseModel):
    id: uuid.UUID
    deck_id: uuid.UUID
    front: CardContent
    back: CardContent

    class Config:
        from_attributes = True

# Schema for reviewing a card
class CardReview(BaseModel):
    card_id: uuid.UUID
    is_correct: bool

# Schema for user statistics
class UserStats(BaseModel):
    total_xp: int
    current_level: int
    badges: List[str] = [] # Simplified for now

# --- Boss Fight Schemas ---

# Simplified card view for the boss fight
class BossFightCard(BaseModel):
    id: uuid.UUID
    front: CardContent
    back: CardContent

    class Config:
        from_attributes = True

# Schema for the initial boss fight session
class BossFightSession(BaseModel):
    boss_hp: int
    cards: List[BossFightCard]

# Schema for submitting an answer during a boss fight
class BossFightAnswer(BaseModel):
    card_id: uuid.UUID
    answer_is_correct: bool # Did the user answer correctly?

# Schema for the result after submitting an answer
class BossFightResult(BaseModel):
    correct: bool
    damage_dealt: int
    boss_hp_remaining: int
    debuff_seconds: int
