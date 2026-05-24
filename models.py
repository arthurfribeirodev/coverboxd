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
    email = Column("email",String, unique=True)
    senha = Column("senha",String,nullable=False)
    pfp = Column("pfp",String)

    def __init__(self, username, email, senha, pfp=None):
        self.username = username
        self.email = email
        self.senha = senha
        self.pfp = pfp

class Genres(Base):
    __tablename__ = "genres"
    id = Column("id",Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column("name",String,nullable=False)
    description = Column("description",String,nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

class Covers(Base):
    __tablename__ = "covers"
    id = Column("id",Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column("name",String,nullable=False)
    description = Column("description",String,nullable=False)
    image_url = Column("image_url",String,nullable=False)
    genre_id = Column("genre_id",Integer, ForeignKey("genres.id"), nullable=False)
    date = Column("date",String,nullable=False)

    def __init__(self, name, description, image_url, genre_id, date):
        self.name = name
        self.description = description
        self.image_url = image_url
        self.genre_id = genre_id
        self.date = date


class Artists(Base):
    __tablename__ = 'artists'
    id = Column("id",Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column("name",String,nullable=False)
    description = Column("description",String,nullable=False)
    image_url = Column("image_url",String,nullable=False)
    genre_id = Column("genre_id",Integer, ForeignKey("genres.id"), nullable=False)

    def __init__(self, name, description, image_url, genre_id):
        self.name = name
        self.description = description
        self.image_url = image_url
        self.genre_id = genre_id

class Rates(Base):
    __tablename__ = "rates"
    id = Column("id",Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column("user_id",Integer, ForeignKey('users.id'), nullable=False)
    cover_id = Column("cover_id",Integer, ForeignKey('covers.id'), nullable=False)
    artist_id = Column("artist_id",Integer, ForeignKey('artists.id'), nullable=False)
    rating = Column("rating",Integer, nullable=False)

    def __init__(self, user_id, cover_id, artist_id, rating):
        self.user_id = user_id
        self.cover_id = cover_id
        self.artist_id = artist_id
        self.rating = rating