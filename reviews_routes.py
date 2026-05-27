from fastapi import APIRouter, Depends

from models import Rates,db
from schemas import ReviewSchema
from dependencies import session_grab

review_router = APIRouter(prefix="/reviews", tags=["reviews"])


 # Rotas para criar, deletar e atualizar reviews
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

@review_router.delete("/review/{review_id}")
async def delete_review(review_id: int, session = Depends(session_grab)):
    review = session.query(Rates).filter(Rates.id == review_id).first()
    if review:
        session.delete(review)
        session.commit()
        return {"message": f"Review com ID {review_id} deletada com sucesso!"}
    else:
        return {"message": f"Review com ID {review_id} não encontrada."}
    

@review_router.patch("/review/{review_id}")
async def update_review(review_id: int, review_schema: ReviewSchema, session = Depends(session_grab)):
    review = session.query(Rates).filter(Rates.id == review_id).first()
    if review:
        review.rating = review_schema.rating
        review.comment = review_schema.comment
        session.commit()
        return {"message": f"Review com ID {review_id} atualizada com sucesso!"}
    else:
        return {"message": f"Review com ID {review_id} não encontrada."}