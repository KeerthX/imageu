import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class CartoonizationTool(ImageProcessingTool):
    def __init__(self):
        # Default cartoonization parameters
        self._num_down = 2  # Number of downsampling steps
        self._num_bilateral = 7  # Number of bilateral filtering steps
        self._edge_threshold = 100  # Threshold for edge detection
        self._color_reduce_levels = 8  # Number of color quantization levels

    def _validate_num_down(self, num_down):
        """Validate number of downsampling steps."""
        try:
            num_down = int(num_down)
            if num_down < 0 or num_down > 5:
                raise ValueError("Number of downsampling steps must be between 0 and 5")
            return num_down
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid number of downsampling steps: {str(e)}")

    def _validate_num_bilateral(self, num_bilateral):
        """Validate number of bilateral filtering steps."""
        try:
            num_bilateral = int(num_bilateral)
            if num_bilateral < 0 or num_bilateral > 10:
                raise ValueError("Number of bilateral filtering steps must be between 0 and 10")
            return num_bilateral
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid number of bilateral filtering steps: {str(e)}")

    def _validate_edge_threshold(self, threshold):
        """Validate edge detection threshold."""
        try:
            threshold = int(threshold)
            if threshold < 0 or threshold > 255:
                raise ValueError("Edge threshold must be between 0 and 255")
            return threshold
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid edge threshold: {str(e)}")

    def _validate_color_reduce_levels(self, levels):
        """Validate color quantization levels."""
        try:
            levels = int(levels)
            if levels < 2 or levels > 32:
                raise ValueError("Color reduce levels must be between 2 and 32")
            return levels
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid color reduce levels: {str(e)}")

    @property
    def num_down(self):
        return self._num_down

    @num_down.setter
    def num_down(self, value):
        self._num_down = self._validate_num_down(value)

    @property
    def num_bilateral(self):
        return self._num_bilateral

    @num_bilateral.setter
    def num_bilateral(self, value):
        self._num_bilateral = self._validate_num_bilateral(value)

    @property
    def edge_threshold(self):
        return self._edge_threshold

    @edge_threshold.setter
    def edge_threshold(self, value):
        self._edge_threshold = self._validate_edge_threshold(value)

    @property
    def color_reduce_levels(self):
        return self._color_reduce_levels

    @color_reduce_levels.setter
    def color_reduce_levels(self, value):
        self._color_reduce_levels = self._validate_color_reduce_levels(value)

    def apply(self, image):
        """Apply cartoonization effect."""
        if image is None:
            raise ValueError("No image provided for processing")
        
        try:
            # Create a copy of the image
            img = image.copy()

            # Downsample image multiple times
            for _ in range(self._num_down):
                img = cv2.pyrDown(img)

            # Apply bilateral filtering multiple times
            for _ in range(self._num_bilateral):
                img = cv2.bilateralFilter(img, 9, 9, 7)

            # Upsample image back to original size
            for _ in range(self._num_down):
                img = cv2.pyrUp(img)

            # Convert to grayscale for edge detection
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect edges
            edges = cv2.medianBlur(cv2.Canny(gray, 50, self._edge_threshold), 3)

            # Color quantization
            img_quant = img.copy()
            for i in range(3):
                img_quant[:,:,i] = img_quant[:,:,i] // self._color_reduce_levels * self._color_reduce_levels

            # Combine color image with edges
            cartoon = cv2.bitwise_and(img_quant, img_quant, mask=~edges)

            return cartoon

        except Exception as e:
            raise RuntimeError(f"Error applying cartoonization: {str(e)}")

    def get_parameters(self):
        """Get current tool parameters."""
        return {
            "num_down": self._num_down,
            "num_bilateral": self._num_bilateral,
            "edge_threshold": self._edge_threshold,
            "color_reduce_levels": self._color_reduce_levels
        }

    def update_parameters(self, params):
        """Update tool parameters."""
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "num_down" in params:
            self.num_down = params["num_down"]
        if "num_bilateral" in params:
            self.num_bilateral = params["num_bilateral"]
        if "edge_threshold" in params:
            self.edge_threshold = params["edge_threshold"]
        if "color_reduce_levels" in params:
            self.color_reduce_levels = params["color_reduce_levels"]