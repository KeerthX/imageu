import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class OilPaintingTool(ImageProcessingTool):
    def __init__(self):
        # Default oil painting effect parameters
        self._brush_size = 5  # Size of the brush/kernel
        self._color_levels = 10  # Number of color intensity levels
        self._smooth_factor = 1  # Smoothing factor

    def _validate_brush_size(self, size):
        """Validate brush size parameter."""
        try:
            size = int(size)
            if size < 3 or size > 21 or size % 2 == 0:
                raise ValueError("Brush size must be an odd number between 3 and 21")
            return size
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid brush size: {str(e)}")

    def _validate_color_levels(self, levels):
        """Validate color levels parameter."""
        try:
            levels = int(levels)
            if levels < 2 or levels > 255:
                raise ValueError("Color levels must be between 2 and 255")
            return levels
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid color levels: {str(e)}")

    def _validate_smooth_factor(self, factor):
        """Validate smoothing factor parameter."""
        try:
            factor = float(factor)
            if factor < 0 or factor > 5:
                raise ValueError("Smooth factor must be between 0 and 5")
            return factor
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid smooth factor: {str(e)}")

    @property
    def brush_size(self):
        return self._brush_size

    @brush_size.setter
    def brush_size(self, value):
        self._brush_size = self._validate_brush_size(value)

    @property
    def color_levels(self):
        return self._color_levels

    @color_levels.setter
    def color_levels(self, value):
        self._color_levels = self._validate_color_levels(value)

    @property
    def smooth_factor(self):
        return self._smooth_factor

    @smooth_factor.setter
    def smooth_factor(self, value):
        self._smooth_factor = self._validate_smooth_factor(value)

    def apply(self, image):
        """Apply oil painting effect."""
        if image is None:
            raise ValueError("No image provided for processing")
        
        try:
            # Create a copy of the image
            img = image.copy()

            # Convert to float for processing
            img_float = img.astype(np.float32) / 255.0

            # Apply Gaussian blur for smoothing
            if self._smooth_factor > 0:
                img_float = cv2.GaussianBlur(
                    img_float, 
                    (0, 0), 
                    sigmaX=self._smooth_factor, 
                    sigmaY=self._smooth_factor
                )

            # Convert to grayscale for intensity calculation
            gray = cv2.cvtColor(img_float, cv2.COLOR_BGR2GRAY)

            # Prepare output image
            oil_painting = np.zeros_like(img)

            # Iterate through each channel
            for channel in range(3):
                # Create a canvas for this channel
                channel_canvas = np.zeros_like(gray)

                # Iterate through image with the specified brush size
                h, w = img.shape[:2]
                for y in range(0, h, self._brush_size):
                    for x in range(0, w, self._brush_size):
                        # Extract local region
                        region = gray[
                            max(0, y-self._brush_size//2):min(h, y+self._brush_size//2+1),
                            max(0, x-self._brush_size//2):min(w, x+self._brush_size//2+1)
                        ]

                        # Find the most frequent intensity level
                        intensity_hist = np.histogram(
                            region, 
                            bins=self._color_levels, 
                            range=(0, 1)
                        )[0]
                        most_frequent_intensity = np.argmax(intensity_hist)

                        # Calculate mean color in this region for the current channel
                        mean_color = np.mean(
                            img[
                                max(0, y-self._brush_size//2):min(h, y+self._brush_size//2+1),
                                max(0, x-self._brush_size//2):min(w, x+self._brush_size//2+1),
                                channel
                            ]
                        )

                        # Fill the region with mean color
                        channel_canvas[
                            max(0, y-self._brush_size//2):min(h, y+self._brush_size//2+1),
                            max(0, x-self._brush_size//2):min(w, x+self._brush_size//2+1)
                        ] = mean_color

                # Assign channel to output image
                oil_painting[:,:,channel] = channel_canvas.astype(np.uint8)

            return oil_painting

        except Exception as e:
            raise RuntimeError(f"Error applying oil painting effect: {str(e)}")

    def get_parameters(self):
        """Get current tool parameters."""
        return {
            "brush_size": self._brush_size,
            "color_levels": self._color_levels,
            "smooth_factor": self._smooth_factor
        }

    def update_parameters(self, params):
        """Update tool parameters."""
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "brush_size" in params:
            self.brush_size = params["brush_size"]
        if "color_levels" in params:
            self.color_levels = params["color_levels"]
        if "smooth_factor" in params:
            self.smooth_factor = params["smooth_factor"]