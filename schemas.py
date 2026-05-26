from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    username: str
    email: str
    senha: str
    pfp: str | None = None
    
    class Config:
        from_attributes = True


class ReviewSchema(BaseModel):
    user_id: int
    cover_id: int
    artist_id: int
    rating: int = Field(...,le=5)
    comment: str | None = None
    
    class Config:
        from_attributes = True

class loginSchema(BaseModel):
    email: str
    senha: str
    
    class Config:
        from_attributes = True