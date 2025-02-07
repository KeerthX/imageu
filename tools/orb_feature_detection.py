# tools/orb_feature_detection_tool.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class ORBFeatureDetectionTool(ImageProcessingTool):
    def __init__(self):
        self._n_features = 500
        self._scale_factor = 1.2
        self._n_levels = 8
        self._edge_threshold = 31
        self._first_level = 0
        self._wta_k = 2
        self._score_type = cv2.ORB_HARRIS_SCORE
        self._patch_size = 31
        self._fast_threshold = 20
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if self._n_features <= 0:
                raise ValueError("Number of features must be positive")
            if self._scale_factor <= 1.0:
                raise ValueError("Scale factor must be greater than 1.0")
            if self._n_levels <= 0:
                raise ValueError("Number of levels must be positive")
            if self._edge_threshold <= 0:
                raise ValueError("Edge threshold must be positive")
            if self._first_level < 0:
                raise ValueError("First level must be non-negative")
            if self._wta_k not in [2, 3, 4]:
                raise ValueError("WTA_K must be 2, 3, or 4")
            if self._score_type not in [cv2.ORB_HARRIS_SCORE, cv2.ORB_FAST_SCORE]:
                raise ValueError("Invalid score type")
            if self._patch_size <= 0:
                raise ValueError("Patch size must be positive")
            if self._fast_threshold <= 0:
                raise ValueError("FAST threshold must be positive")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
            
        try:
            # Create ORB detector
            orb = cv2.ORB_create(
                nfeatures=self._n_features,
                scaleFactor=self._scale_factor,
                nlevels=self._n_levels,
                edgeThreshold=self._edge_threshold,
                firstLevel=self._first_level,
                WTA_K=self._wta_k,
                scoreType=self._score_type,
                patchSize=self._patch_size,
                fastThreshold=self._fast_threshold
            )
            
            # Find keypoints
            keypoints = orb.detect(image, None)
            
            # Compute descriptors
            keypoints, descriptors = orb.compute(image, keypoints)
            
            # Draw keypoints
            result = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0),
                                     flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
            
            return result
            
        except Exception as e:
            raise RuntimeError(f"Error applying ORB feature detection: {str(e)}")

    def get_parameters(self):
        return {
            "n_features": self._n_features,
            "scale_factor": self._scale_factor,
            "n_levels": self._n_levels,
            "edge_threshold": self._edge_threshold,
            "first_level": self._first_level,
            "wta_k": self._wta_k,
            "score_type": self._score_type,
            "patch_size": self._patch_size,
            "fast_threshold": self._fast_threshold
        }

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        for key, value in params.items():
            if hasattr(self, f"_{key}"):
                setattr(self, f"_{key}", value)
        
        self._validate_parameters()