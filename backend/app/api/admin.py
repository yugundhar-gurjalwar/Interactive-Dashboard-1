from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any
from app.api import deps
from app.db import models
from app.schemas import user as user_schemas

router = APIRouter()

@router.get("/users", response_model=List[user_schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users. Only for superusers.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough privileges")
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.delete("/users/{user_id}", response_model=user_schemas.User)
def delete_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a user. Only for superusers.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough privileges")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user
