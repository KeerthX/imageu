import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class DehazingTool(ImageProcessingTool):
    def __init__(self):
        # Default dehazing parameters
        self._transmission_weight = 0.95  # Transmission weight
        self._attenuation_factor = 0.1  # Attenuation factor
        self._max_filter_size = 81  # Maximum filter size for dark channel prior
        self._omega = 0.75  # Global atmospheric light estimation parameter
        self._algorithm = 'dark_channel'  # Dehazing algorithm type

    def _validate_transmission_weight(self, weight):
        """Validate transmission weight parameter."""
        try:
            weight = float(weight)
            if weight < 0 or weight > 1:
                raise ValueError("Transmission weight must be between 0 and 1")
            return weight
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid transmission weight: {str(e)}")

    def _validate_attenuation_factor(self, factor):
        """Validate attenuation factor parameter."""
        try:
            factor = float(factor)
            if factor < 0 or factor > 1:
                raise ValueError("Attenuation factor must be between 0 and 1")
            return factor
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid attenuation factor: {str(e)}")

    def _validate_max_filter_size(self, size):
        """Validate maximum filter size."""
        try:
            size = int(size)
            if size < 3 or size > 201 or size % 2 == 0:
                raise ValueError("Max filter size must be an odd number between 3 and 201")
            return size
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid max filter size: {str(e)}")

    def _validate_omega(self, omega):
        """Validate omega parameter."""
        try:
            omega = float(omega)
            if omega < 0 or omega > 1:
                raise ValueError("Omega must be between 0 and 1")
            return omega
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid omega value: {str(e)}")

    def _validate_algorithm(self, algorithm):
        """Validate dehazing algorithm."""
        valid_algorithms = ['dark_channel', 'guided_filter']
        if algorithm not in valid_algorithms:
            raise ValueError(f"Algorithm must be one of {valid_algorithms}")
        return algorithm

    @property
    def transmission_weight(self):
        return self._transmission_weight

    @transmission_weight.setter
    def transmission_weight(self, value):
        self._transmission_weight = self._validate_transmission_weight(value)

    @property
    def attenuation_factor(self):
        return self._attenuation_factor

    @attenuation_factor.setter
    def attenuation_factor(self, value):
        self._attenuation_factor = self._validate_attenuation_factor(value)

    @property
    def max_filter_size(self):
        return self._max_filter_size

    @max_filter_size.setter
    def max_filter_size(self, value):
        self._max_filter_size = self._validate_max_filter_size(value)

    @property
    def omega(self):
        return self._omega

    @omega.setter
    def omega(self, value):
        self._omega = self._validate_omega(value)

    @property
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        self._algorithm = self._validate_algorithm(value)

    def _dark_channel_prior(self, image):
        """Compute dark channel prior."""
        # Minimum filter in RGB channels
        dark_channel = np.min(image, axis=2)
        dark_channel = cv2.erode(dark_channel, np.ones((self._max_filter_size, self._max_filter_size)))
        return dark_channel

    def _estimate_atmospheric_light(self, image, dark_channel):
        """Estimate global atmospheric light."""
        flat_dark = dark_channel.ravel()
        flat_image = image.reshape(-1, 3)
        
        # Find top pixels
        top_dark_indices = np.argsort(flat_dark)[-int(len(flat_dark) * self._omega):]
        atmospheric_light = np.mean(flat_image[top_dark_indices], axis=0)
        
        return atmospheric_light

    def apply(self, image):
        """Apply dehazing effect."""
        if image is None:
            raise ValueError("No image provided for processing")
        
        try:
            # Normalize image to float
            img = image.astype(np.float32) / 255.0

            # Compute dark channel prior
            dark_channel = self._dark_channel_prior(img)

            # Estimate atmospheric light
            atmospheric_light = self._estimate_atmospheric_light(img, dark_channel)

            # Compute transmission map
            normalized_img = img / atmospheric_light
            transmission = 1 - self._transmission_weight * np.min(normalized_img, axis=2)

            # Guided filter refinement (optional)
            if self._algorithm == 'guided_filter':
                # Simple guided filtering to refine transmission map
                transmission = cv2.ximgproc.guidedFilter(
                    img.astype(np.uint8), 
                    transmission.astype(np.float32), 
                    15, 
                    self._attenuation_factor
                )

            # Recover scene radiance
            recovered = np.zeros_like(img)
            for i in range(3):
                recovered[:,:,i] = (img[:,:,i] - atmospheric_light[i]) / np.maximum(transmission, 0.1) + atmospheric_light[i]

            # Clip and convert back to uint8
            recovered = np.clip(recovered * 255, 0, 255).astype(np.uint8)

            return recovered

        except Exception as e:
            raise RuntimeError(f"Error applying dehazing: {str(e)}")

    def get_parameters(self):
        """Get current tool parameters."""
        return {
            "transmission_weight": self._transmission_weight,
            "attenuation_factor": self._attenuation_factor,
            "max_filter_size": self._max_filter_size,
            "omega": self._omega,
            "algorithm": self._algorithm
        }

    def update_parameters(self, params):
        """Update tool parameters."""
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "transmission_weight" in params:
            self.transmission_weight = params["transmission_weight"]
        if "attenuation_factor" in params:
            self.attenuation_factor = params["attenuation_factor"]
        if "max_filter_size" in params:
            self.max_filter_size = params["max_filter_size"]
        if "omega" in params:
            self.omega = params["omega"]
        if "algorithm" in params:
            self.algorithm = params["algorithm"]