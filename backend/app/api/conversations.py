from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from app.api import deps
from app.db import models
from app.schemas import conversation as conversation_schemas

router = APIRouter()

@router.post("/", response_model=conversation_schemas.Conversation)
def create_conversation(
    conversation_in: conversation_schemas.ConversationCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    conversation = models.Conversation(
        title=conversation_in.title,
        user_id=current_user.id
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

@router.get("/", response_model=List[conversation_schemas.Conversation])
def read_conversations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    conversations = db.query(models.Conversation).filter(
        models.Conversation.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return conversations

@router.get("/{conversation_id}", response_model=conversation_schemas.Conversation)
def read_conversation(
    conversation_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    conversation = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id,
        models.Conversation.user_id == current_user.id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.delete("/{conversation_id}", response_model=conversation_schemas.Conversation)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    conversation = db.query(models.Conversation).filter(
        models.Conversation.id == conversation_id,
        models.Conversation.user_id == current_user.id
    ).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    db.delete(conversation)
    db.commit()
    return conversation
