from sqlalchemy import Column, Integer, String, MetaData, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


# Criar Database
db = create_engine('sqlite:///database.db')

# Criar Base

Base = declarative_base()

# Criação de Tabelas

class Users(Base):
    __tablename__ = 'users'
    id = Column("id",Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column("username",String,nullable=False)
    email = Column("email",String, unique=True)
    senha = Column("senha",String,nullable=False)

class Genres(Base):
    __tablename__ = 'genres'
    id = Column("id",Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column("name",String,nullable=False)
    description = Column("description",String,nullable=False)

class Covers(Base):
    __tablename__ = 'covers'
    id = Column("id",Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column("name",String,nullable=False)
    description = Column("description",String,nullable=False)
    image_url = Column("image_url",String,nullable=False)
    genre_id = Column("genre_id",Integer, ForeignKey('genres.id'), nullable=False)
    date = Column("date",String,nullable=False)


class Artists(Base):
    __tablename__ = 'artists'
    id = Column("id",Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column("name",String,nullable=False)
    description = Column("description",String,nullable=False)
    image_url = Column("image_url",String,nullable=False)
    genre_id = Column("genre_id",Integer, ForeignKey('genres.id'), nullable=False)

class Rates(Base):
    __tablename__ = 'rates'
    id = Column("id",Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column("user_id",Integer, ForeignKey('users.id'), nullable=False)
    cover_id = Column("cover_id",Integer, ForeignKey('covers.id'), nullable=False)
    artist_id = Column("artist_id",Integer, ForeignKey('artists.id'), nullable=False)
    rating = Column("rating",Integer, nullable=False)