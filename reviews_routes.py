from fastapi import APIRouter, Depends, HTTPException

from models import Rates,db
from schemas import ReviewSchema, UpdateReviewSchema
from dependencies import session_grab, verify_token

review_router = APIRouter(prefix="/reviews", tags=["reviews"])


 # Rotas para criar, deletar e atualizar reviews
@review_router.post("/review")
async def create_review(review_schema: ReviewSchema, session = Depends(session_grab), user_id: int = Depends(verify_token)):
    new_review = Rates(
        user_id=user_id.id,
        cover_id=review_schema.cover_id,
        artist_id=review_schema.artist_id,
        rating=review_schema.rating,
        comment=review_schema.comment
    )
    session.add(new_review)
    session.commit()
    return {"message": f"Review criada com sucesso! ID: {new_review.id}"}

@review_router.delete("/review/delete/{review_id}")
async def delete_review(review_id: int, session = Depends(session_grab)):
    review = session.query(Rates).filter(Rates.id == review_id).first()
    if review:
        session.delete(review)
        session.commit()
        return {"message": f"Review com ID {review_id} deletada com sucesso!"}
    else:
        return {"message": f"Review com ID {review_id} não encontrada."}
    

@review_router.patch("/review/update/{review_id}")
async def update_review(review_id: int, update_schema: UpdateReviewSchema, session = Depends(session_grab)):
    review = session.query(Rates).filter(Rates.id == review_id).first()
    if review:
        review.rating = update_schema.rating
        review.comment = update_schema.comment
        session.commit()
        return {"message": f"Review com ID {review_id} atualizada com sucesso!"}
    else:
        return {"message": f"Review com ID {review_id} não encontrada."}
    
@review_router.get("/reviews/{review_id}")
async def get_review(review_id: int, session = Depends(session_grab)):
    review = session.query(Rates).filter(Rates.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail=f"Review ID {review_id} não encontrada.")
    return review