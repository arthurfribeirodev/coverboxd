from fastapi import APIRouter
from spotify_service import buscar_cove

albuns_router = APIRouter(prefix="/albuns", tags=["albuns"])

    # Rota para buscar álbuns

@albuns_router.get("/search/{query}")
async def search_albuns(query: str):
    results = buscar_cove(query)
    return {"albuns": results}