from fastapi import APIRouter, Depends

from models import Rates,db
from schemas import ReviewSchema
from dependencies import session_grab

review_router = APIRouter(prefix="/reviews", tags=["reviews"])



@review_router.post("/review")
async def create_review(review_schema: ReviewSchema, session = Depends(session_grab)):
    new_review = Rates(
        user_id=review_schema.user_id,
        cover_id=review_schema.cover_id,
        artist_id=review_schema.artist_id,
        rating=review_schema.rating,
        comment=review_schema.comment
    )
    session.add(new_review)
    session.commit()
    return {"message": f"Review criada com sucesso! ID: {new_review.id}"}