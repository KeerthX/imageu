# tools/pencil_sketch.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class PencilSketchTool(ImageProcessingTool):
    def __init__(self):
        # Default pencil sketch parameters
        self._sketch_mode = 'grayscale'  # Sketch mode (grayscale or color)
        self._sigma_s = 60  # Sigma spatial parameter for edge preservation
        self._sigma_r = 0.07  # Sigma range parameter for color/intensity preservation
        self._edge_threshold = 50  # Threshold for edge detection
        self._shade_factor = 0.1  # Shading intensity factor

    def _validate_sigma_s(self, sigma):
        """Validate sigma spatial parameter."""
        try:
            sigma = float(sigma)
            if sigma <= 0 or sigma > 200:
                raise ValueError("Sigma spatial must be between 0 and 200")
            return sigma
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid sigma spatial: {str(e)}")

    def _validate_sigma_r(self, sigma):
        """Validate sigma range parameter."""
        try:
            sigma = float(sigma)
            if sigma <= 0 or sigma > 1:
                raise ValueError("Sigma range must be between 0 and 1")
            return sigma
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid sigma range: {str(e)}")

    def _validate_edge_threshold(self, threshold):
        """Validate edge detection threshold."""
        try:
            threshold = int(threshold)
            if threshold < 0 or threshold > 255:
                raise ValueError("Edge threshold must be between 0 and 255")
            return threshold
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid edge threshold: {str(e)}")

    def _validate_shade_factor(self, factor):
        """Validate shading factor."""
        try:
            factor = float(factor)
            if factor < 0 or factor > 1:
                raise ValueError("Shade factor must be between 0 and 1")
            return factor
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid shade factor: {str(e)}")

    def _validate_sketch_mode(self, mode):
        """Validate sketch mode."""
        valid_modes = ['grayscale', 'color']
        if mode not in valid_modes:
            raise ValueError(f"Sketch mode must be one of {valid_modes}")
        return mode

    @property
    def sigma_s(self):
        return self._sigma_s

    @sigma_s.setter
    def sigma_s(self, value):
        self._sigma_s = self._validate_sigma_s(value)

    @property
    def sigma_r(self):
        return self._sigma_r

    @sigma_r.setter
    def sigma_r(self, value):
        self._sigma_r = self._validate_sigma_r(value)

    @property
    def edge_threshold(self):
        return self._edge_threshold

    @edge_threshold.setter
    def edge_threshold(self, value):
        self._edge_threshold = self._validate_edge_threshold(value)

    @property
    def shade_factor(self):
        return self._shade_factor

    @shade_factor.setter
    def shade_factor(self, value):
        self._shade_factor = self._validate_shade_factor(value)

    @property
    def sketch_mode(self):
        return self._sketch_mode

    @sketch_mode.setter
    def sketch_mode(self, value):
        self._sketch_mode = self._validate_sketch_mode(value)

    def apply(self, image):
        """Apply pencil sketch effect."""
        if image is None:
            raise ValueError("No image provided for processing")
        
        try:
            # Create a copy of the image
            img = image.copy()

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Invert grayscale image
            inverted = 255 - gray

            # Apply Gaussian blur
            blurred = cv2.GaussianBlur(inverted, (21, 21), 0)

            # Dodge blend
            def dodge_blend(front, back):
                final_sketch = cv2.divide(front, 255 - back, scale=256)
                return final_sketch

            # Create pencil sketch
            if self._sketch_mode == 'grayscale':
                # Grayscale pencil sketch
                pencil_sketch = dodge_blend(blurred, gray)
            else:
                # Color pencil sketch
                # Apply bilateral filter for edge preservation
                bilateral = cv2.bilateralFilter(
                    img, 
                    9, 
                    self._sigma_s, 
                    self._sigma_r
                )

                # Convert bilateral filtered image to grayscale
                bilateral_gray = cv2.cvtColor(bilateral, cv2.COLOR_BGR2GRAY)

                # Invert grayscale bilateral image
                bilateral_inverted = 255 - bilateral_gray

                # Blur the inverted image
                bilateral_blurred = cv2.GaussianBlur(bilateral_inverted, (21, 21), 0)

                # Dodge blend for color sketch
                pencil_sketch = dodge_blend(bilateral_blurred, bilateral_gray)

                # Add color to the sketch
                pencil_sketch = cv2.cvtColor(pencil_sketch, cv2.COLOR_GRAY2BGR)

            # Apply shade factor to control sketch intensity
            pencil_sketch = np.clip(
                pencil_sketch * (1 + self._shade_factor), 
                0, 
                255
            ).astype(np.uint8)

            return pencil_sketch

        except Exception as e:
            raise RuntimeError(f"Error applying pencil sketch effect: {str(e)}")

    def get_parameters(self):
        """Get current tool parameters."""
        return {
            "sketch_mode": self._sketch_mode,
            "sigma_s": self._sigma_s,
            "sigma_r": self._sigma_r,
            "edge_threshold": self._edge_threshold,
            "shade_factor": self._shade_factor
        }

    def update_parameters(self, params):
        """Update tool parameters."""
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "sketch_mode" in params:
            self.sketch_mode = params["sketch_mode"]
        if "sigma_s" in params:
            self.sigma_s = params["sigma_s"]
        if "sigma_r" in params:
            self.sigma_r = params["sigma_r"]
        if "edge_threshold" in params:
            self.edge_threshold = params["edge_threshold"]
        if "shade_factor" in params:
            self.shade_factor = params["shade_factor"]