from tools.resize import ResizeTool
from tools.filter import FilterTool
from tools.rotate import RotateTool


class ToolManager:
    def __init__(self):
        self.tools = {
            "Resize": ResizeTool(),
            "Filter": FilterTool(),
            "Rotate": RotateTool()
        }

    def get_available_tools(self):
        return list(self.tools.keys())

    def get_tool(self, name):
        return self.tools[name]
