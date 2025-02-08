# tools/fast_corner_detection.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class FASTCornerDetectionTool(ImageProcessingTool):
    def __init__(self):
        # Default FAST parameters
        self._threshold = 10  # Threshold for corner detection
        self._non_max_suppression = True  # Enable non-maximum suppression
        self._type = cv2.FAST_FEATURE_DETECTOR_TYPE_9_16  # FAST feature type

    def _validate_threshold(self, threshold):
        """Validate threshold parameter."""
        try:
            threshold = int(threshold)
            if threshold < 0 or threshold > 255:
                raise ValueError("Threshold must be between 0 and 255")
            return threshold
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid threshold: {str(e)}")

    def _validate_feature_type(self, feature_type):
        """Validate FAST feature detector type."""
        valid_types = [
            cv2.FAST_FEATURE_DETECTOR_TYPE_5_8,
            cv2.FAST_FEATURE_DETECTOR_TYPE_7_12,
            cv2.FAST_FEATURE_DETECTOR_TYPE_9_16
        ]
        try:
            feature_type = int(feature_type)
            if feature_type not in valid_types:
                raise ValueError(f"Invalid FAST feature detector type. Must be one of {valid_types}")
            return feature_type
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid feature type: {str(e)}")

    @property
    def threshold(self):
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        self._threshold = self._validate_threshold(value)

    @property
    def non_max_suppression(self):
        return self._non_max_suppression

    @non_max_suppression.setter
    def non_max_suppression(self, value):
        if not isinstance(value, bool):
            raise ValueError("Non-maximum suppression must be a boolean")
        self._non_max_suppression = value

    @property
    def feature_type(self):
        return self._type

    @feature_type.setter
    def feature_type(self, value):
        self._type = self._validate_feature_type(value)

    def apply(self, image):
        """Apply FAST corner detection."""
        if image is None:
            raise ValueError("No image provided for processing")
        
        try:
            # Convert to grayscale if needed
            if len(image.shape) > 2:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image

            # Create FAST detector
            fast = cv2.FastFeatureDetector_create(
                threshold=self._threshold,
                nonmaxSuppression=self._non_max_suppression,
                type=self._type
            )

            # Detect keypoints
            keypoints = fast.detect(gray)

            # Draw keypoints on the original image
            output_image = cv2.drawKeypoints(
                image, 
                keypoints, 
                None, 
                color=(0, 255, 0),  # Green color for keypoints
                flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
            )

            return output_image

        except Exception as e:
            raise RuntimeError(f"Error applying FAST corner detection: {str(e)}")

    def get_parameters(self):
        """Get current tool parameters."""
        return {
            "threshold": self._threshold,
            "non_max_suppression": self._non_max_suppression,
            "feature_type": self._type
        }

    def update_parameters(self, params):
        """Update tool parameters."""
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "threshold" in params:
            self.threshold = params["threshold"]
        if "non_max_suppression" in params:
            self.non_max_suppression = params["non_max_suppression"]
        if "feature_type" in params:
            self.feature_type = params["feature_type"]