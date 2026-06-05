from fastapi import APIRouter, Depends, HTTPException
from models import Covers
from spotify_service import buscar_cove
from dependencies import session_grab
from schemas import AlbumSchema, AlbumUpdateSchema

albuns_router = APIRouter(prefix="/albuns", tags=["albuns"])

    # Rota para buscar álbuns

@albuns_router.get("/search/{query}")
async def search_albuns(query: str):
    results = buscar_cove(query)
    return {"albuns": results}
@albuns_router.get("/")
async def get_albuns(session = Depends(session_grab)):
    albuns = session.query(Covers).all()
    return albuns    

@albuns_router.post("/")
async def create_album(album : AlbumSchema, session = Depends(session_grab)):
    new_album = Covers(
        name=album.name,
        artist=album.artist,
        image_url=album.image_url
    )
    session.add(new_album)
    session.commit()
    return {"message": f"Álbum criado com sucesso! ID: {new_album.id}"}

@albuns_router.patch("/{album_id}")
async def update_album(album_id: str, upd_album : AlbumUpdateSchema, session = Depends(session_grab)):
    update = session.query(Covers).filter(Covers.id == album_id).first()
    if not update:
        return {"message": f"Álbum com ID {album_id} não encontrado."}
    if upd_album.name is not None:
        update.name = upd_album.name
    if upd_album.artist is not None:
        update.artist = upd_album.artist
    if upd_album.image_url is not None:
        update.image_url = upd_album.image_url
    session.commit()
    return {"message": f"Álbum de ID {album_id} atualizado!"}

@albuns_router.delete("/{album_id}")
async def delete_album(album_id: int, session = Depends(session_grab)):
    del_album = session.query(Covers).filter(Covers.id == album_id).first()
    if not del_album:
        raise HTTPException(status_code=404, detail=f"Álbum com ID {album_id} não encontrado.")
    session.delete(del_album)
    session.commit()
    return {"message": f"Álbum de ID {album_id} deletado!"}


    