# tools./surf_feature_detection.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class SURFFeatureDetectionTool(ImageProcessingTool):
    def __init__(self):
        # Default SURF parameters
        self._hessian_threshold = 100  # Hessian threshold for feature detection
        self._n_octaves = 4  # Number of pyramid octaves
        self._n_octave_layers = 3  # Number of layers in each octave
        self._extended = False  # Extended descriptor flag
        self._upright = False  # Rotation invariance flag

    def _validate_hessian_threshold(self, threshold):
        """Validate Hessian threshold parameter."""
        try:
            threshold = float(threshold)
            if threshold <= 0:
                raise ValueError("Hessian threshold must be a positive number")
            return threshold
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid Hessian threshold: {str(e)}")

    def _validate_n_octaves(self, n_octaves):
        """Validate number of octaves parameter."""
        try:
            n_octaves = int(n_octaves)
            if n_octaves <= 0:
                raise ValueError("Number of octaves must be a positive integer")
            return n_octaves
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid number of octaves: {str(e)}")

    def _validate_n_octave_layers(self, n_octave_layers):
        """Validate number of octave layers parameter."""
        try:
            n_octave_layers = int(n_octave_layers)
            if n_octave_layers <= 0:
                raise ValueError("Number of octave layers must be a positive integer")
            return n_octave_layers
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid number of octave layers: {str(e)}")

    @property
    def hessian_threshold(self):
        return self._hessian_threshold

    @hessian_threshold.setter
    def hessian_threshold(self, value):
        self._hessian_threshold = self._validate_hessian_threshold(value)

    @property
    def n_octaves(self):
        return self._n_octaves

    @n_octaves.setter
    def n_octaves(self, value):
        self._n_octaves = self._validate_n_octaves(value)

    @property
    def n_octave_layers(self):
        return self._n_octave_layers

    @n_octave_layers.setter
    def n_octave_layers(self, value):
        self._n_octave_layers = self._validate_n_octave_layers(value)

    @property
    def extended(self):
        return self._extended

    @extended.setter
    def extended(self, value):
        if not isinstance(value, bool):
            raise ValueError("Extended flag must be a boolean")
        self._extended = value

    @property
    def upright(self):
        return self._upright

    @upright.setter
    def upright(self, value):
        if not isinstance(value, bool):
            raise ValueError("Upright flag must be a boolean")
        self._upright = value

    def apply(self, image):
        """Apply SURF feature detection."""
        if image is None:
            raise ValueError("No image provided for processing")
        
        try:
            # Convert to grayscale if needed
            if len(image.shape) > 2:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image

            # Create SURF detector
            surf = cv2.xfeatures2d.SURF_create(
                hessianThreshold=self._hessian_threshold,
                nOctaves=self._n_octaves,
                nOctaveLayers=self._n_octave_layers,
                extended=self._extended,
                upright=self._upright
            )

            # Detect keypoints and compute descriptors
            keypoints, descriptors = surf.detectAndCompute(gray, None)

            # Draw keypoints on the original image
            output_image = cv2.drawKeypoints(
                image, 
                keypoints, 
                None, 
                flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
            )

            return output_image

        except Exception as e:
            raise RuntimeError(f"Error applying SURF feature detection: {str(e)}")

    def get_parameters(self):
        """Get current tool parameters."""
        return {
            "hessian_threshold": self._hessian_threshold,
            "n_octaves": self._n_octaves,
            "n_octave_layers": self._n_octave_layers,
            "extended": self._extended,
            "upright": self._upright
        }

    def update_parameters(self, params):
        """Update tool parameters."""
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "hessian_threshold" in params:
            self.hessian_threshold = params["hessian_threshold"]
        if "n_octaves" in params:
            self.n_octaves = params["n_octaves"]
        if "n_octave_layers" in params:
            self.n_octave_layers = params["n_octave_layers"]
        if "extended" in params:
            self.extended = params["extended"]
        if "upright" in params:
            self.upright = params["upright"]