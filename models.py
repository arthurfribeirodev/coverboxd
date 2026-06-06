from sqlalchemy import Column, Integer, String, MetaData, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


# Criar Database
db = create_engine('sqlite:///database.db')

# Criar Base

Base = declarative_base()

# Criação de Tabelas

class Users(Base):
    __tablename__ = "users"
    id = Column("id",Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column("username",String,nullable=False)
    email = Column("email",String, nullable=False)
    senha = Column("senha",String,nullable=False)
    pfp = Column("pfp",String)

    def __init__(self, username, email, senha, pfp=None):
        self.username = username
        self.email = email
        self.senha = senha
        self.pfp = pfp


class Covers(Base):
    __tablename__ = "covers"
    id = Column("id",Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column("name",String,nullable=False)
    image_url = Column("image_url",String,nullable=False)
    artist = Column("artist",String,nullable=False)

    def __init__(self, name, artist, image_url):
        self.name = name
        self.artist = artist
        self.image_url = image_url


class Rates(Base):
    __tablename__ = "rates"
    id = Column("id",Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column("user_id",Integer, ForeignKey('users.id'), nullable=False)
    cover_id = Column("cover_id",Integer, ForeignKey('covers.id'), nullable=False)
    rating = Column("rating",Integer, nullable=False)
    comment = Column("comment",String)

    def __init__(self, user_id, cover_id,rating, comment):
        self.user_id = user_id
        self.cover_id = cover_id
        self.rating = rating
        self.comment = comment