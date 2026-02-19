from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas import chat as chat_schemas
from app.services.llm.providers import LLMProvider, LLMFactory
from app.db import models
from typing import AsyncGenerator

router = APIRouter()

async def stream_and_save(
    generator: AsyncGenerator[str, None], 
    db: Session, 
    conversation_id: int
):
    full_response = ""
    try:
        async for chunk in generator:
            full_response += chunk
            yield chunk
        
        # Save assistant message after stream completes
        db_message = models.Message(
            conversation_id=conversation_id,
            role="assistant",
            content=full_response
        )
        db.add(db_message)
        db.commit()
    except Exception as e:
        print(f"Error saving stream: {e}")
        # Optionally log error
        pass

@router.post("/completions", response_model=chat_schemas.ChatResponse)
async def chat_completion(
    request: chat_schemas.ChatRequest,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    # 1. Handle Conversation ID
    conversation_id = request.conversation_id
    if not conversation_id:
        # Create new conversation
        title = request.messages[0].content[:30] + "..." if request.messages else "New Chat"
        conversation = models.Conversation(title=title, user_id=current_user.id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        conversation_id = conversation.id
    else:
        # Verify ownership
        conversation = db.query(models.Conversation).filter(
            models.Conversation.id == conversation_id,
            models.Conversation.user_id == current_user.id
        ).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")

    # 2. Save User Message
    if request.messages:
        last_message = request.messages[-1]
        if last_message.role == "user":
            user_msg = models.Message(
                conversation_id=conversation_id,
                role="user",
                content=last_message.content
            )
            db.add(user_msg)
            db.add(user_msg)
            db.commit()

            # Safety Check
            from app.services.safety.guardian import safety_guardian
            if not safety_guardian.check_input(last_message.content):
                # Log violation
                log = models.SecurityLog(
                    user_id=current_user.id,
                    action="message",
                    content=last_message.content[:500], # Truncate if too long
                    reason="forbidden_keyword"
                )
                db.add(log)
                db.commit()
                
                # Create assistant response denying request
                db_message = models.Message(
                    conversation_id=conversation_id,
                    role="assistant",
                    content="I cannot fulfill this request as it violates safety guidelines."
                )
                db.add(db_message)
                db.commit()
                
                if request.stream:
                    async def deny_stream():
                        yield "I cannot fulfill this request as it violates safety guidelines."
                    return StreamingResponse(
                        deny_stream(),
                        media_type="text/event-stream"
                    )
                else:
                    return {"content": "I cannot fulfill this request as it violates safety guidelines.", "conversation_id": conversation_id}

    # 3. Generate Response
    provider = LLMFactory.get_provider()
    
    # Get available tools
    from app.services.tools.registry import tool_registry
    tools = list(tool_registry._tools.values())
    
    # Convert messages to dict format
    # TODO: Fetch history from DB if needed, for now using request messages
    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    if request.stream:
        return StreamingResponse(
            stream_and_save(
                provider.generate_stream(messages, request.model, tools=tools),
                db,
                conversation_id
            ),
            media_type="text/event-stream"
        )
    else:
        content = await provider.generate(messages, request.model, tools=tools)
        
        # Save complete response
        db_message = models.Message(
            conversation_id=conversation_id,
            role="assistant",
            content=content
        )
        db.add(db_message)
        db.commit()
        
        return {"content": content, "conversation_id": conversation_id}
