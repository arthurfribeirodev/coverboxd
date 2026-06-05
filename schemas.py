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

    #Schema de Update
class UpdateUserSchema(BaseModel):
    username: str | None = None
    email: str | None = None
    senha: str | None = None
    pfp: str | None = None

    class Config:
        from_attributes = True    

    #Schema da Review
class ReviewSchema(BaseModel):
    cover_id: int
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
    rating: int = Field(...,le=5)
    comment: str | None = None
    
    class Config:
        from_attributes = True

class AlbumSchema(BaseModel):
    name: str
    image_url: str
    artist: str
    
    class Config:
        from_attributes = True

class AlbumUpdateSchema(BaseModel):
    name: str | None = None
    image_url: str | None = None
    artist: str | None = None
    
    class Config:
        from_attributes = True