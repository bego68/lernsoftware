from sqlalchemy.orm import Session
from . import database, schemas, security
from .database import models
from datetime import datetime, timedelta

# --- User CRUD ---

def get_user_by_username(db: Session, username: str):
    """
    Fetches a user by their username.
    """
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """
    Fetches a user by their email.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates a new user in the database.
    """
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Learning Logic (SRS) CRUD ---

def get_due_cards_for_user(db: Session, user_id: str):
    """
    Fetches all cards that are due for review for a specific user.
    A card is due if its next_review date is in the past.
    It also includes cards the user has never reviewed before.
    """
    # Subquery to find all cards the user has already reviewed
    reviewed_cards_subquery = db.query(models.UserProgress.card_id).filter(models.UserProgress.user_id == user_id)

    # Cards that are due
    due_cards = db.query(models.Card).join(models.UserProgress).filter(
        models.UserProgress.user_id == user_id,
        models.UserProgress.next_review <= datetime.utcnow()
    ).all()

    # Cards the user has never seen (limit to 10 new cards per session to avoid overload)
    new_cards = db.query(models.Card).filter(
        models.Card.id.notin_(reviewed_cards_subquery)
    ).limit(10).all()

    return due_cards + new_cards

def get_or_create_user_progress(db: Session, user_id: str, card_id: str):
    """
    Gets the UserProgress for a card. If it doesn't exist, it creates a new one.
    """
    user_progress = db.query(models.UserProgress).filter_by(user_id=user_id, card_id=card_id).first()

    if not user_progress:
        # First time seeing this card, create a progress entry
        user_progress = models.UserProgress(
            user_id=user_id,
            card_id=card_id,
            current_box=1,
            next_review=datetime.utcnow() # Due immediately
        )
        db.add(user_progress)
        db.commit()
        db.refresh(user_progress)

    return user_progress

def update_user_progress(db: Session, user_progress: models.UserProgress, is_correct: bool):
    """
    Updates the user's progress on a card based on their answer (correct/incorrect).
    Implements the Leitner System logic for spaced repetition.
    """
    if is_correct:
        # Move card to the next box
        user_progress.current_box += 1
    else:
        # If incorrect, move card back to the first box
        user_progress.current_box = 1

    # Calculate next review date based on the box number (Leitner formula: I = 2^(b-1))
    days_to_add = 2 ** (user_progress.current_box - 1)
    user_progress.next_review = datetime.utcnow() + timedelta(days=days_to_add)

    db.commit()
    db.refresh(user_progress)
    return user_progress

def update_user_xp(db: Session, user: models.User, difficulty: int, streak_multiplier: float = 1.0):
    """
    Updates the user's XP based on the card difficulty and streak multiplier.
    XPgain = (Difficulty × 10) × Streak-Multiplier
    """
    xp_gain = int((difficulty * 10) * streak_multiplier)
    user.total_xp += xp_gain

    # Simple level up logic: new level every 1000 XP
    if user.total_xp >= user.current_level * 1000:
        user.current_level += 1

    db.commit()
    db.refresh(user)
    return user

# --- Boss Fight CRUD ---

def get_random_cards_for_boss_fight(db: Session, count: int = 10):
    """
    Selects a specified number of random cards for a boss fight.
    """
    # This is a simple approach. For large datasets, this can be slow.
    # A more performant way would be to get random IDs or use a DB-specific function.
    from sqlalchemy.sql.expression import func
    return db.query(models.Card).order_by(func.rand()).limit(count).all()

def create_or_update_boss_fight_session(db: Session, user_id: str, boss_hp: int):
    """
    Creates or updates a boss fight session for a user.
    """
    session = db.query(models.BossFightSession).filter_by(user_id=user_id).first()
    if session:
        session.boss_hp = boss_hp
        session.started_at = datetime.utcnow()
    else:
        session = models.BossFightSession(user_id=user_id, boss_hp=boss_hp)
        db.add(session)
    db.commit()
    db.refresh(session)
    return session

def get_boss_fight_session(db: Session, user_id: str):
    """
    Gets the active boss fight session for a user.
    """
    return db.query(models.BossFightSession).filter_by(user_id=user_id).first()

def delete_boss_fight_session(db: Session, user_id: str):
    """
    Deletes the boss fight session for a user.
    """
    session = db.query(models.BossFightSession).filter_by(user_id=user_id).first()
    if session:
        db.delete(session)
        db.commit()
