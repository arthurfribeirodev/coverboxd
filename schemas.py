from pydantic import BaseModel, Field

 # Schemas para organização e validação de dados

    #Schema do usuário
class UserSchema(BaseModel):
    username: str
    email: str
    senha: str
    pfp: str | None = None
    
    class Config:
        from_attributes = True

    #Schema da Review
class ReviewSchema(BaseModel):
    user_id: int
    cover_id: int
    artist_id: int
    rating: int = Field(...,le=5)
    comment: str | None = None
    
    class Config:
        from_attributes = True
    
    #Schema de login
class loginSchema(BaseModel):
    email: str
    senha: str
    
    class Config:
        from_attributes = True

    #Schema para atualização de review
class UpdateReviewSchema(BaseModel):
    review_id: int
    rating: int = Field(...,le=5)
    comment: str | None = None
    
    class Config:
        from_attributes = True