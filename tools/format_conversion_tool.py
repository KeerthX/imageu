# tools/format_conversion_tool.py
import cv2
import os
import imghdr
import numpy as np

class FormatConversionTool:
    """Tool for converting images between different formats."""
    
    def __init__(self):
        self._parameters = {
            'output_format': 'PNG'
        }
        self.supported_formats = {
            'PNG': '.png',
            'JPEG': '.jpg',
            'BMP': '.bmp',
            'TIFF': '.tiff'
        }
        # Format-specific quality parameters
        self.format_params = {
            'PNG': cv2.IMWRITE_PNG_COMPRESSION,  # 0-9 (default 3)
            'JPEG': cv2.IMWRITE_JPEG_QUALITY,    # 0-100 (default 95)
            'TIFF': cv2.IMWRITE_TIFF_COMPRESSION # 1-32946 (default 1)
        }
        
    def get_parameters(self):
        """Get current parameters."""
        return self._parameters
        
    def update_parameters(self, parameters):
        """Update tool parameters."""
        if 'output_format' in parameters:
            if parameters['output_format'] not in self.supported_formats:
                raise ValueError(f"Unsupported format: {parameters['output_format']}")
            self._parameters['output_format'] = parameters['output_format']
    
    @staticmethod
    def detect_format(image_path):
        """
        Detect the format of the input image.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            str: Detected format name (PNG, JPEG, BMP, TIFF, or Unknown)
        """
        try:
            # Try using imghdr first for more accurate detection
            detected = imghdr.what(image_path)
            if detected:
                format_map = {
                    'png': 'PNG',
                    'jpeg': 'JPEG',
                    'bmp': 'BMP',
                    'tiff': 'TIFF'
                }
                return format_map.get(detected, detected.upper())
            
            # Fallback to checking file extension
            ext = os.path.splitext(image_path)[1].lower()
            format_map = {
                '.png': 'PNG',
                '.jpg': 'JPEG',
                '.jpeg': 'JPEG',
                '.bmp': 'BMP',
                '.tiff': 'TIFF',
                '.tif': 'TIFF'
            }
            return format_map.get(ext, 'Unknown')
        except Exception:
            return 'Unknown'
    
    def get_format_parameters(self, format_name):
        """
        Get format-specific parameters for saving images.
        
        Args:
            format_name (str): Name of the format (PNG, JPEG, etc.)
            
        Returns:
            list: List of parameters for cv2.imwrite
        """
        params = []
        if format_name in self.format_params:
            if format_name == 'PNG':
                params.extend([self.format_params[format_name], 3])  # Default compression
            elif format_name == 'JPEG':
                params.extend([self.format_params[format_name], 95])  # High quality
            elif format_name == 'TIFF':
                params.extend([self.format_params[format_name], 1])  # Default compression
        return params
    
    def apply(self, image):
        """
        Apply the format conversion. Note that actual conversion happens during save.
        This method just returns the original image.
        
        Args:
            image (numpy.ndarray): Input image
            
        Returns:
            numpy.ndarray: Original image (unchanged)
        """
        return image.copy()

    def save(self, image, output_path):
        """
        Save the image in the specified format.
        
        Args:
            image (numpy.ndarray): Image to save
            output_path (str): Path where to save the image
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            format_name = self._parameters['output_format']
            params = self.get_format_parameters(format_name)
            
            # Ensure correct file extension
            base, _ = os.path.splitext(output_path)
            output_path = base + self.supported_formats[format_name]
            
            # Save with format-specific parameters
            success = cv2.imwrite(output_path, image, params)
            
            if not success:
                raise RuntimeError(f"Failed to save image as {format_name}")
                
            return True
            
        except Exception as e:
            raise RuntimeError(f"Error saving image: {str(e)}")