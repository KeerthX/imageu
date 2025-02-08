# tools/sift_feature_detection.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class SIFTFeatureDetectionTool(ImageProcessingTool):
    def __init__(self):
        # Default SIFT parameters
        self._n_features = 0  # Number of best features to retain
        self._n_octave_layers = 3  # Number of layers in each octave
        self._contrast_threshold = 0.04  # Contrast threshold for feature detection
        self._edge_threshold = 10  # Threshold for filtering out edge-like features
        self._sigma = 1.6  # Gaussian blur sigma

    def _validate_n_features(self, n_features):
        """Validate number of features parameter."""
        try:
            n_features = int(n_features)
            if n_features < 0:
                raise ValueError("Number of features must be non-negative")
            return n_features
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid number of features: {str(e)}")

    def _validate_n_octave_layers(self, n_octave_layers):
        """Validate number of octave layers parameter."""
        try:
            n_octave_layers = int(n_octave_layers)
            if n_octave_layers <= 0:
                raise ValueError("Number of octave layers must be a positive integer")
            return n_octave_layers
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid number of octave layers: {str(e)}")

    def _validate_contrast_threshold(self, threshold):
        """Validate contrast threshold parameter."""
        try:
            threshold = float(threshold)
            if threshold < 0 or threshold > 1:
                raise ValueError("Contrast threshold must be between 0 and 1")
            return threshold
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid contrast threshold: {str(e)}")

    def _validate_edge_threshold(self, threshold):
        """Validate edge threshold parameter."""
        try:
            threshold = float(threshold)
            if threshold <= 0:
                raise ValueError("Edge threshold must be a positive number")
            return threshold
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid edge threshold: {str(e)}")

    def _validate_sigma(self, sigma):
        """Validate Gaussian blur sigma parameter."""
        try:
            sigma = float(sigma)
            if sigma <= 0:
                raise ValueError("Sigma must be a positive number")
            return sigma
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid sigma value: {str(e)}")

    @property
    def n_features(self):
        return self._n_features

    @n_features.setter
    def n_features(self, value):
        self._n_features = self._validate_n_features(value)

    @property
    def n_octave_layers(self):
        return self._n_octave_layers

    @n_octave_layers.setter
    def n_octave_layers(self, value):
        self._n_octave_layers = self._validate_n_octave_layers(value)

    @property
    def contrast_threshold(self):
        return self._contrast_threshold

    @contrast_threshold.setter
    def contrast_threshold(self, value):
        self._contrast_threshold = self._validate_contrast_threshold(value)

    @property
    def edge_threshold(self):
        return self._edge_threshold

    @edge_threshold.setter
    def edge_threshold(self, value):
        self._edge_threshold = self._validate_edge_threshold(value)

    @property
    def sigma(self):
        return self._sigma

    @sigma.setter
    def sigma(self, value):
        self._sigma = self._validate_sigma(value)

    def apply(self, image):
        """Apply SIFT feature detection."""
        if image is None:
            raise ValueError("No image provided for processing")
        
        try:
            # Convert to grayscale if needed
            if len(image.shape) > 2:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image

            # Create SIFT detector
            sift = cv2.SIFT_create(
                nfeatures=self._n_features,
                nOctaveLayers=self._n_octave_layers,
                contrastThreshold=self._contrast_threshold,
                edgeThreshold=self._edge_threshold,
                sigma=self._sigma
            )

            # Detect keypoints and compute descriptors
            keypoints, descriptors = sift.detectAndCompute(gray, None)

            # Draw keypoints on the original image
            output_image = cv2.drawKeypoints(
                image, 
                keypoints, 
                None, 
                flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
            )

            return output_image

        except Exception as e:
            raise RuntimeError(f"Error applying SIFT feature detection: {str(e)}")

    def get_parameters(self):
        """Get current tool parameters."""
        return {
            "n_features": self._n_features,
            "n_octave_layers": self._n_octave_layers,
            "contrast_threshold": self._contrast_threshold,
            "edge_threshold": self._edge_threshold,
            "sigma": self._sigma
        }

    def update_parameters(self, params):
        """Update tool parameters."""
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "n_features" in params:
            self.n_features = params["n_features"]
        if "n_octave_layers" in params:
            self.n_octave_layers = params["n_octave_layers"]
        if "contrast_threshold" in params:
            self.contrast_threshold = params["contrast_threshold"]
        if "edge_threshold" in params:
            self.edge_threshold = params["edge_threshold"]
        if "sigma" in params:
            self.sigma = params["sigma"]