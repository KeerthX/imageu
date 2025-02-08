# tools/pixelation.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class PixelationTool(ImageProcessingTool):
    def __init__(self):
        # Default pixelation parameters
        self._pixel_size = 10  # Size of pixels for pixelation effect
        self._scale_factor = 0.1  # Scale factor for pixelation

    def _validate_pixel_size(self, size):
        """Validate pixel size parameter."""
        try:
            size = int(size)
            if size < 2 or size > 100:
                raise ValueError("Pixel size must be between 2 and 100")
            return size
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid pixel size: {str(e)}")

    def _validate_scale_factor(self, factor):
        """Validate scale factor parameter."""
        try:
            factor = float(factor)
            if factor <= 0 or factor > 1:
                raise ValueError("Scale factor must be between 0 and 1")
            return factor
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid scale factor: {str(e)}")

    @property
    def pixel_size(self):
        return self._pixel_size

    @pixel_size.setter
    def pixel_size(self, value):
        self._pixel_size = self._validate_pixel_size(value)

    @property
    def scale_factor(self):
        return self._scale_factor

    @scale_factor.setter
    def scale_factor(self, value):
        self._scale_factor = self._validate_scale_factor(value)

    def apply(self, image):
        """Apply pixelation effect."""
        if image is None:
            raise ValueError("No image provided for processing")
        
        try:
            # Create a copy of the image
            img = image.copy()

            # Calculate small image dimensions
            small_width = int(img.shape[1] * self._scale_factor)
            small_height = int(img.shape[0] * self._scale_factor)

            # Resize the image down
            small_img = cv2.resize(img, (small_width, small_height), interpolation=cv2.INTER_LINEAR)

            # Resize back up using nearest neighbor to create pixelation effect
            pixelated = cv2.resize(
                small_img, 
                (img.shape[1], img.shape[0]), 
                interpolation=cv2.INTER_NEAREST
            )

            # Alternative pixelation method using mean pooling
            if self._pixel_size > 1:
                h, w = img.shape[:2]
                pixelated = np.zeros_like(img)
                for i in range(0, h, self._pixel_size):
                    for j in range(0, w, self._pixel_size):
                        # Extract block
                        block = img[i:i+self._pixel_size, j:j+self._pixel_size]
                        
                        # Compute mean color of the block
                        mean_color = np.mean(block, axis=(0, 1)).astype(np.uint8)
                        
                        # Fill block with mean color
                        pixelated[i:i+self._pixel_size, j:j+self._pixel_size] = mean_color

            return pixelated

        except Exception as e:
            raise RuntimeError(f"Error applying pixelation: {str(e)}")

    def get_parameters(self):
        """Get current tool parameters."""
        return {
            "pixel_size": self._pixel_size,
            "scale_factor": self._scale_factor
        }

    def update_parameters(self, params):
        """Update tool parameters."""
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "pixel_size" in params:
            self.pixel_size = params["pixel_size"]
        if "scale_factor" in params:
            self.scale_factor = params["scale_factor"]