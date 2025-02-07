# tools/non_local_means_denoising.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class NonLocalMeansDenoisingTool(ImageProcessingTool):
    def __init__(self):
        self._h = 10  # Filter strength
        self._template_window_size = 7
        self._search_window_size = 21
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if not isinstance(self._h, (int, float)) or self._h <= 0:
                raise ValueError("Filter strength (h) must be positive")
            if not isinstance(self._template_window_size, int) or self._template_window_size < 1:
                raise ValueError("Template window size must be positive")
            if not isinstance(self._search_window_size, int) or self._search_window_size < 1:
                raise ValueError("Search window size must be positive")
            if self._search_window_size <= self._template_window_size:
                raise ValueError("Search window size must be larger than template window size")
        except Exception as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def parameters(self):
        return {
            "h": self._h,
            "template_window_size": self._template_window_size,
            "search_window_size": self._search_window_size
        }

    @parameters.setter
    def parameters(self, values):
        if not isinstance(values, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        if "h" in values:
            self._h = float(values["h"])
        if "template_window_size" in values:
            self._template_window_size = int(values["template_window_size"])
        if "search_window_size" in values:
            self._search_window_size = int(values["search_window_size"])
        self._validate_parameters()

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        try:
            return cv2.fastNlMeansDenoisingColored(
                image,
                None,
                h=self._h,
                hColor=self._h,
                templateWindowSize=self._template_window_size,
                searchWindowSize=self._search_window_size
            )
        except Exception as e:
            raise RuntimeError(f"Error applying Non-Local Means denoising: {str(e)}")

    def get_parameters(self):
        return self.parameters

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        self.parameters = params