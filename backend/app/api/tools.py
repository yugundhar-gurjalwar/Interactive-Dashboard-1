from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
from app.api import deps
from app.services.tools.registry import tool_registry

router = APIRouter()

class ToolExecutionRequest(BaseModel):
    name: str
    arguments: Dict[str, Any]

@router.get("/", response_model=List[Dict[str, Any]])
def list_tools(current_user = Depends(deps.get_current_active_user)):
    return tool_registry.list_tools()

@router.post("/execute")
def execute_tool(
    request: ToolExecutionRequest,
    current_user = Depends(deps.get_current_active_user)
):
    tool = tool_registry.get_tool(request.name)
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool '{request.name}' not found")
    
    try:
        # Validate arguments using Pydantic model
        validated_args = tool.args_schema(**request.arguments)
        result = tool.run(**validated_args.model_dump())
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
