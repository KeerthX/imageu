from tools.resize import ResizeTool
from tools.filter import FilterTool
from tools.rotate import RotateTool
from tools.brightness import BrightnessTool
from tools.contrast import ContrastTool
from tools.sharpen import SharpenTool


class ToolManager:
    def __init__(self):
        self.tools = {
            "Resize": ResizeTool(),
            "Filter": FilterTool(),
            "Rotate": RotateTool(),
            "Brightness": BrightnessTool(),
            "Contrast": ContrastTool(),
            "Sharpen": SharpenTool(),
        }

    def get_available_tools(self):
        return list(self.tools.keys())

    def get_tool(self, name):
        return self.tools[name]
