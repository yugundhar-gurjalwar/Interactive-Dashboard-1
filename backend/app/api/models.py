from fastapi import APIRouter, HTTPException
import httpx
from app.core.config import settings

router = APIRouter()

@router.get("/")
async def list_models():
    """
    Proxy to Ollama /api/tags to list available models.
    """
    url = f"{settings.OLLAMA_BASE_URL}/api/tags"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            if response.status_code != 200:
                 raise HTTPException(status_code=502, detail="Failed to fetch models from Ollama")
            
            data = response.json()
            # Transform if needed, or return as is.
            # Ollama returns {"models": [{"name": "llama3:latest", ...}]}
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to Ollama: {str(e)}")
