import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class EmbossingTool(ImageProcessingTool):
    def __init__(self):
        # Default embossing parameters
        self._emboss_angle = 45  # Embossing angle in degrees
        self._emboss_depth = 2  # Depth of embossing effect
        self._background_gray = 128  # Background gray level
        self._emboss_type = 'standard'  # Embossing type (standard, enhanced)

    def _validate_emboss_angle(self, angle):
        """Validate embossing angle parameter."""
        try:
            angle = float(angle)
            if angle < 0 or angle > 360:
                raise ValueError("Emboss angle must be between 0 and 360 degrees")
            return angle
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid emboss angle: {str(e)}")

    def _validate_emboss_depth(self, depth):
        """Validate embossing depth parameter."""
        try:
            depth = float(depth)
            if depth < 0 or depth > 10:
                raise ValueError("Emboss depth must be between 0 and 10")
            return depth
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid emboss depth: {str(e)}")

    def _validate_background_gray(self, gray):
        """Validate background gray level."""
        try:
            gray = int(gray)
            if gray < 0 or gray > 255:
                raise ValueError("Background gray must be between 0 and 255")
            return gray
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid background gray: {str(e)}")

    def _validate_emboss_type(self, emboss_type):
        """Validate embossing type."""
        valid_types = ['standard', 'enhanced']
        if emboss_type not in valid_types:
            raise ValueError(f"Emboss type must be one of {valid_types}")
        return emboss_type

    @property
    def emboss_angle(self):
        return self._emboss_angle

    @emboss_angle.setter
    def emboss_angle(self, value):
        self._emboss_angle = self._validate_emboss_angle(value)

    @property
    def emboss_depth(self):
        return self._emboss_depth

    @emboss_depth.setter
    def emboss_depth(self, value):
        self._emboss_depth = self._validate_emboss_depth(value)

    @property
    def background_gray(self):
        return self._background_gray

    @background_gray.setter
    def background_gray(self, value):
        self._background_gray = self._validate_background_gray(value)

    @property
    def emboss_type(self):
        return self._emboss_type

    @emboss_type.setter
    def emboss_type(self, value):
        self._emboss_type = self._validate_emboss_type(value)

    def apply(self, image):
        """Apply embossing effect."""
        if image is None:
            raise ValueError("No image provided for processing")
        
        try:
            # Convert to grayscale
            if len(image.shape) > 2:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image

            # Create embossing kernels based on angle
            angle_rad = np.deg2rad(self._emboss_angle)
            dx = np.cos(angle_rad)
            dy = np.sin(angle_rad)

            # Standard embossing kernel
            if self._emboss_type == 'standard':
                kernel = np.array([
                    [-1, -1, 0],
                    [-1, 0, 1],
                    [0, 1, 1]
                ], dtype=np.float32)
            else:  # Enhanced embossing
                kernel = np.array([
                    [-2, -1, 0],
                    [-1, 0, 1],
                    [0, 1, 2]
                ], dtype=np.float32)

            # Scale kernel by depth
            kernel *= self._emboss_depth

            # Apply convolution
            embossed = cv2.filter2D(gray, -1, kernel)

            # Add background gray level
            embossed = embossed + self._background_gray
            embossed = np.clip(embossed, 0, 255).astype(np.uint8)

            # Convert back to 3-channel if original was color
            if len(image.shape) > 2:
                embossed = cv2.cvtColor(embossed, cv2.COLOR_GRAY2BGR)

            return embossed

        except Exception as e:
            raise RuntimeError(f"Error applying embossing effect: {str(e)}")

    def get_parameters(self):
        """Get current tool parameters."""
        return {
            "emboss_angle": self._emboss_angle,
            "emboss_depth": self._emboss_depth,
            "background_gray": self._background_gray,
        }

    def update_parameters(self, params):
        """Update tool parameters."""
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "emboss_angle" in params:
            self.emboss_angle = params["emboss_angle"]
        if "emboss_depth" in params:
            self.emboss_depth = params["emboss_depth"]
        if "background_gray" in params:
            self.background_gray = params["background_gray"]