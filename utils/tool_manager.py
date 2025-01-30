# utils/tool_manager.py

from tools.filter_tool import FilterTool
from tools.brightness_tool import BrightnessTool

class ToolManager:
    def __init__(self):
        self.tools = {
            "Gaussian Filter": FilterTool,
            "Brightness Adjustment": BrightnessTool
        }

    def get_available_tools(self):
        return list(self.tools.keys())

    def get_tool(self, name):
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")
        try:
            return self.tools[name]()
        except Exception as e:
            raise RuntimeError(f"Error creating tool {name}: {str(e)}")