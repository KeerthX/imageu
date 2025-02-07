# tools/gradient_tool.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class GradientTool(ImageProcessingTool):
    def __init__(self):
        self._gradient_type = 'sobel'
        self._kernel_size = 3
        self._direction = 'both'
        self._validate_parameters(self._gradient_type, self._kernel_size, self._direction)

    def _validate_parameters(self, gradient_type, kernel_size, direction):
        try:
            kernel_size = int(kernel_size)
            if kernel_size not in [1, 3, 5, 7]:
                raise ValueError("Kernel size must be 1, 3, 5, or 7")
            
            valid_types = ['sobel', 'scharr', 'laplacian']
            if gradient_type not in valid_types:
                raise ValueError(f"Gradient type must be one of {valid_types}")
                
            valid_directions = ['x', 'y', 'both']
            if direction not in valid_directions:
                raise ValueError(f"Direction must be one of {valid_directions}")
                
            return gradient_type, kernel_size, direction
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    @property
    def gradient_type(self):
        return self._gradient_type

    @gradient_type.setter
    def gradient_type(self, value):
        self._gradient_type, _, _ = self._validate_parameters(value, self._kernel_size, self._direction)

    @property
    def kernel_size(self):
        return self._kernel_size

    @kernel_size.setter
    def kernel_size(self, value):
        _, self._kernel_size, _ = self._validate_parameters(self._gradient_type, value, self._direction)

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        _, _, self._direction = self._validate_parameters(self._gradient_type, self._kernel_size, value)

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
            
        try:
            if len(image.shape) > 2:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image

            if self._gradient_type == 'sobel':
                if self._direction == 'x':
                    grad = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=self._kernel_size)
                elif self._direction == 'y':
                    grad = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=self._kernel_size)
                else:
                    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=self._kernel_size)
                    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=self._kernel_size)
                    grad = np.sqrt(grad_x**2 + grad_y**2)
            
            elif self._gradient_type == 'scharr':
                if self._direction == 'x':
                    grad = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
                elif self._direction == 'y':
                    grad = cv2.Scharr(gray, cv2.CV_64F, 0, 1)
                else:
                    grad_x = cv2.Scharr(gray, cv2.CV_64F, 1, 0)
                    grad_y = cv2.Scharr(gray, cv2.CV_64F, 0, 1)
                    grad = np.sqrt(grad_x**2 + grad_y**2)
            
            else:  # laplacian
                grad = cv2.Laplacian(gray, cv2.CV_64F, ksize=self._kernel_size)

            # Convert back to uint8
            grad = cv2.convertScaleAbs(grad)
            return grad
            
        except Exception as e:
            raise RuntimeError(f"Error applying gradient: {str(e)}")

    def get_parameters(self):
        return {
            "gradient_type": self._gradient_type,
            "kernel_size": self._kernel_size,
            "direction": self._direction
        }

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        current_type = self._gradient_type
        current_size = self._kernel_size
        current_dir = self._direction
        
        if "gradient_type" in params:
            current_type = params["gradient_type"]
        if "kernel_size" in params:
            current_size = params["kernel_size"]
        if "direction" in params:
            current_dir = params["direction"]
            
        # Validate all parameters together
        self._gradient_type, self._kernel_size, self._direction = \
            self._validate_parameters(current_type, current_size, current_dir)

