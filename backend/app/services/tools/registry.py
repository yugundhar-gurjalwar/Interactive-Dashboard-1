from typing import Dict, Type, List, Any
from app.services.tools.base import Tool
from app.services.tools.definitions import WebSearchTool, CalculatorTool, WebsiteReaderTool, FileReaderTool, NotesTool, ReminderTool

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        self.register_tools()

    def register_tools(self):
        tools_to_register = [
            WebSearchTool(),
            CalculatorTool(),
            WebsiteReaderTool(),
            FileReaderTool(),
            NotesTool(),
            ReminderTool()
        ]
        for tool in tools_to_register:
            self.register_tool(tool)

    def register_tool(self, tool: Tool):
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Tool:
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": tool.name, 
                "description": tool.description,
                "args_schema": tool.args_schema.schema()
            }
            for tool in self._tools.values()
        ]

tool_registry = ToolRegistry()
