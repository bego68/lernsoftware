from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..database.database import get_db
from ..dependencies import get_current_user
from ..database import models

router = APIRouter(
    tags=["Cards & Learning"]
)

@router.get("/cards/due", response_model=List[schemas.Card])
def get_due_cards(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    Fetches all due learning cards for the current user, including new cards.
    """
    return crud.get_due_cards_for_user(db=db, user_id=current_user.id)

@router.post("/cards/review", status_code=status.HTTP_204_NO_CONTENT)
def review_card(review: schemas.CardReview, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    Submits the result of a card review, updates progress, and awards XP.
    """
    # Get or create the progress entry for this user and card
    user_progress = crud.get_or_create_user_progress(db=db, user_id=current_user.id, card_id=review.card_id)

    # Update the progress based on the Leitner system
    crud.update_user_progress(db=db, user_progress=user_progress, is_correct=review.is_correct)

    if review.is_correct:
        # Award XP for correct answers
        card = user_progress.card # The relationship is loaded
        crud.update_user_xp(db=db, user=current_user, difficulty=card.base_difficulty)

    return

@router.post("/boss-fight/start", response_model=schemas.BossFightSession)
def start_boss_fight(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    Initiates a new Boss-Fight session.
    - Selects 10 random cards.
    - Sets the boss's HP.
    - Stores the session in the database.
    """
    cards = crud.get_random_cards_for_boss_fight(db)
    if len(cards) < 10:
        raise HTTPException(status_code=400, detail="Not enough cards in the database to start a boss fight.")

    # Boss HP = sum of card difficulties * 15
    total_difficulty = sum(card.base_difficulty for card in cards)
    boss_hp = total_difficulty * 15

    # Store the session state in the database
    crud.create_or_update_boss_fight_session(db, user_id=current_user.id, boss_hp=boss_hp)

    return schemas.BossFightSession(boss_hp=boss_hp, cards=cards)

@router.post("/boss-fight/answer", response_model=schemas.BossFightResult)
def answer_boss_fight_card(answer: schemas.BossFightAnswer, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    Processes an answer during a boss fight.
    - Calculates damage based on card difficulty.
    - Applies a time debuff for incorrect answers.
    - Updates the boss's HP in the database.
    """
    session = crud.get_boss_fight_session(db, user_id=current_user.id)
    if not session:
        raise HTTPException(status_code=404, detail="No active boss fight found for this user.")

    card = db.query(models.Card).filter(models.Card.id == answer.card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found.")

    damage_dealt = 0
    debuff_seconds = 0

    if answer.answer_is_correct:
        damage_dealt = card.base_difficulty * 10
        session.boss_hp -= damage_dealt
    else:
        debuff_seconds = 10

    if session.boss_hp <= 0:
        crud.update_user_xp(db, user=current_user, difficulty=50, streak_multiplier=2.0) # 1000 XP bonus
        crud.delete_boss_fight_session(db, user_id=current_user.id)
    else:
        db.commit()

    return schemas.BossFightResult(
        correct=answer.answer_is_correct,
        damage_dealt=damage_dealt,
        boss_hp_remaining=max(0, session.boss_hp),
        debuff_seconds=debuff_seconds
    )


@router.get("/user/stats", response_model=schemas.UserStats)
def get_user_stats(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """
    (Placeholder) Fetches the current user's stats (XP, level, badges).
    """
    # TODO: Implement logic to fetch achievements/badges
    return schemas.UserStats(
        total_xp=current_user.total_xp,
        current_level=current_user.current_level,
        badges=["Neuling"] # Example badge
    )
