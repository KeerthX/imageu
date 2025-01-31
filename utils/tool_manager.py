# utils/tool_manager.py

from tools.filter_tool import FilterTool
from tools.brightness_tool import BrightnessTool
from tools.resize_tool import ResizeTool
from tools.contrast_tool import ContrastTool
from tools.edge_detection_tool import EdgeDetectionTool
from tools.invert_colors_tool import InvertColorsTool
from tools.sharpen_tool import SharpenTool
from tools.grayscale_tool import GrayscaleTool
from tools.flip_tool import FlipTool
from tools.histogram_equalization_tool import HistogramEqualizationTool
from tools.noise_reduction_tool import NoiseReductionTool
from tools.threshold_tool import ThresholdTool
from tools.sepia_tool import SepiaTool

class ToolManager:
    def __init__(self):
        self.tools = {
            "Gaussian Filter": FilterTool,
            "Brightness Adjustment": BrightnessTool,
            "Resize": ResizeTool,
            "Contrast": ContrastTool,
            "Edge Detection": EdgeDetectionTool,
            "Invert Colors": InvertColorsTool,
            "Sharpen": SharpenTool,
            "Grayscale": GrayscaleTool,
            "Flip": FlipTool,
            "Histogram Equalization": HistogramEqualizationTool,
            "Noise Reduction": NoiseReductionTool,
            "Thresholding": ThresholdTool,
            "Sepia Effect": SepiaTool,
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
