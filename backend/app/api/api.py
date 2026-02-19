from fastapi import APIRouter
from app.api import auth, chat, memory, tools, admin, conversations, models

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(memory.router, prefix="/memory", tags=["memory"])
api_router.include_router(tools.router, prefix="/tools", tags=["tools"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(models.router, prefix="/models", tags=["models"])
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
