# tools/hough_transform_tool.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class HoughTransformTool(ImageProcessingTool):
    def __init__(self):
        self._transform_type = 'lines'
        self._rho = 1
        self._theta = np.pi/180
        self._threshold = 100
        self._min_line_length = 100
        self._max_line_gap = 10
        self._dp = 1
        self._min_dist = 50
        self._param1 = 50
        self._param2 = 30
        self._min_radius = 0
        self._max_radius = 0
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if self._transform_type not in ['lines', 'circles']:
                raise ValueError("Transform type must be 'lines' or 'circles'")
            
            if self._rho <= 0:
                raise ValueError("Rho must be positive")
            
            if self._theta <= 0:
                raise ValueError("Theta must be positive")
            
            if self._threshold <= 0:
                raise ValueError("Threshold must be positive")
            
            if self._transform_type == 'lines':
                if self._min_line_length < 0:
                    raise ValueError("Min line length must be non-negative")
                if self._max_line_gap < 0:
                    raise ValueError("Max line gap must be non-negative")
            
            if self._transform_type == 'circles':
                if self._dp <= 0:
                    raise ValueError("DP must be positive")
                if self._min_dist <= 0:
                    raise ValueError("Min distance must be positive")
                if self._param1 <= 0 or self._param2 <= 0:
                    raise ValueError("Circle detection parameters must be positive")
                if self._min_radius < 0:
                    raise ValueError("Min radius must be non-negative")
                if self._max_radius < self._min_radius:
                    raise ValueError("Max radius must be greater than or equal to min radius")
                    
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
            
        try:
            # Convert to grayscale if needed
            if len(image.shape) > 2:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Edge detection
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            
            # Create color image for drawing
            result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            
            if self._transform_type == 'lines':
                lines = cv2.HoughLinesP(edges, self._rho, self._theta, self._threshold,
                                      minLineLength=self._min_line_length,
                                      maxLineGap=self._max_line_gap)
                if lines is not None:
                    for line in lines:
                        x1, y1, x2, y2 = line[0]
                        cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            else:  # circles
                circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, self._dp,
                                         self._min_dist, param1=self._param1,
                                         param2=self._param2,
                                         minRadius=self._min_radius,
                                         maxRadius=self._max_radius)
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for circle in circles[0, :]:
                        center = (circle[0], circle[1])
                        radius = circle[2]
                        cv2.circle(result, center, radius, (0, 255, 0), 2)
            
            return result
            
        except Exception as e:
            raise RuntimeError(f"Error applying Hough transform: {str(e)}")

    def get_parameters(self):
        params = {
            "transform_type": self._transform_type,
            "threshold": self._threshold
        }
        
        if self._transform_type == 'lines':
            params.update({
                "rho": self._rho,
                "theta": self._theta,
                "min_line_length": self._min_line_length,
                "max_line_gap": self._max_line_gap
            })
        else:
            params.update({
                "dp": self._dp,
                "min_dist": self._min_dist,
                "param1": self._param1,
                "param2": self._param2,
                "min_radius": self._min_radius,
                "max_radius": self._max_radius
            })
        
        return params

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        for key, value in params.items():
            if hasattr(self, f"_{key}"):
                setattr(self, f"_{key}", value)
        
        self._validate_parameters()