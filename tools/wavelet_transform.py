import cv2
import numpy as np
import pywt
from .base_tool import ImageProcessingTool

class WaveletTransformTool(ImageProcessingTool):
    def __init__(self):
        self._wavelet = 'haar'
        self._level = 1
        self._mode = 'symmetric'
        self._validate_parameters()

    def _validate_parameters(self):
        try:
            if self._level <= 0:
                raise ValueError("Decomposition level must be positive")
            discrete_wavelets = pywt.wavelist(kind='discrete')
            if self._wavelet not in discrete_wavelets:
                raise ValueError(f"Invalid wavelet type. Must be one of: {', '.join(discrete_wavelets)}")
            if self._mode not in ['zero', 'constant', 'symmetric', 'periodic', 'smooth', 'periodization']:
                raise ValueError("Invalid mode")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid parameters: {str(e)}")

    def apply(self, image):
        if image is None:
            raise ValueError("No image provided for processing")
        
        try:
            if len(image.shape) > 2:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            coeffs = pywt.wavedec2(image, self._wavelet, level=self._level, mode=self._mode)
            
            # Reconstruct image from coefficients
            reconstructed = pywt.waverec2(coeffs, self._wavelet, mode=self._mode)
            
            # Normalize output to 0-255 range
            reconstructed = np.uint8(cv2.normalize(reconstructed, None, 0, 255, cv2.NORM_MINMAX))
            return reconstructed
        except Exception as e:
            raise RuntimeError(f"Error applying Wavelet Transform: {str(e)}")

    def get_parameters(self):
        return {
            "wavelet": self._wavelet,
            "level": self._level,
            "mode": self._mode
        }

    def update_parameters(self, params):
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "wavelet" in params:
            self._wavelet = str(params["wavelet"])
        if "level" in params:
            self._level = int(params["level"])
        if "mode" in params:
            self._mode = str(params["mode"])
        
        self._validate_parameters()

    def get_valid_options(self):
        """Return valid options for parameters that require a drop-down menu."""
        discrete_wavelets = pywt.wavelist(kind='discrete')
        return {
            "wavelet": discrete_wavelets,
            "mode": ['zero', 'constant', 'symmetric', 'periodic', 'smooth', 'periodization']
        }