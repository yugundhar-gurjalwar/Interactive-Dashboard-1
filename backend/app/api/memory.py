from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel
from app.api import deps
from app.services.memory.vector_store import vector_store
from app.db import models

router = APIRouter()

class MemoryCreate(BaseModel):
    text: str

class MemoryResponse(BaseModel):
    id: int
    text: str
    created_at: str

class MemorySearchRequest(BaseModel):
    query: str
    limit: int = 5

@router.post("/", response_model=MemoryResponse)
def add_memory(
    item: MemoryCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    # 1. Save to SQL
    db_memory = models.Memory(
        content=item.text,
        user_id=current_user.id
    )
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)

    # 2. Save to Vector Store
    vector_store.add_memory(
        memory_id=str(db_memory.id),
        text=item.text,
        user_id=current_user.id,
        metadata={"created_at": str(db_memory.created_at)}
    )

    return {
        "id": db_memory.id,
        "text": db_memory.content,
        "created_at": str(db_memory.created_at)
    }

@router.get("/", response_model=List[MemoryResponse])
def get_memories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    memories = db.query(models.Memory).filter(
        models.Memory.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return [
        {
            "id": m.id,
            "text": m.content,
            "created_at": str(m.created_at)
        } for m in memories
    ]

@router.post("/search", response_model=List[Dict[str, Any]])
def search_memory(
    request: MemorySearchRequest,
    current_user: models.User = Depends(deps.get_current_active_user)
):
    results = vector_store.search_memory(
        query=request.query,
        user_id=current_user.id,
        n_results=request.limit
    )
    return results

@router.delete("/{memory_id}")
def delete_memory(
    memory_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    # 1. Delete from SQL
    memory = db.query(models.Memory).filter(
        models.Memory.id == memory_id,
        models.Memory.user_id == current_user.id
    ).first()
    
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
        
    db.delete(memory)
    db.commit()

    # 2. Delete from Vector Store
    vector_store.delete_memory(str(memory_id), current_user.id)

    return {"status": "success", "message": "Memory deleted"}
