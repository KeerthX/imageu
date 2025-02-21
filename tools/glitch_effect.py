# tools/glitch_effect.py
import cv2
import numpy as np
from .base_tool import ImageProcessingTool

class GlitchEffectTool(ImageProcessingTool):
    def __init__(self):
        # Default glitch effect parameters
        self._glitch_intensity = 0.1  # Glitch effect intensity
        self._channel_shift = 10  # Maximum pixel shift
        self._seed = None  # Random seed for reproducibility
        self._glitch_type = 'random'  # Type of glitch effect
        self._block_size = 10  # Size of glitch blocks

    def _validate_glitch_intensity(self, intensity):
        """Validate glitch intensity parameter."""
        try:
            intensity = float(intensity)
            if intensity < 0 or intensity > 1:
                raise ValueError("Glitch intensity must be between 0 and 1")
            return intensity
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid glitch intensity: {str(e)}")

    def _validate_channel_shift(self, shift):
        """Validate channel shift parameter."""
        try:
            shift = int(shift)
            if shift < 0 or shift > 50:
                raise ValueError("Channel shift must be between 0 and 50")
            return shift
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid channel shift: {str(e)}")

    def _validate_block_size(self, size):
        """Validate glitch block size."""
        try:
            size = int(size)
            if size < 1 or size > 50:
                raise ValueError("Block size must be between 1 and 50")
            return size
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid block size: {str(e)}")

    def _validate_glitch_type(self, glitch_type):
        """Validate glitch type."""
        valid_types = ['random', 'block', 'channel', 'slice']
        if glitch_type not in valid_types:
            raise ValueError(f"Glitch type must be one of {valid_types}")
        return glitch_type

    @property
    def glitch_intensity(self):
        return self._glitch_intensity

    @glitch_intensity.setter
    def glitch_intensity(self, value):
        self._glitch_intensity = self._validate_glitch_intensity(value)

    @property
    def channel_shift(self):
        return self._channel_shift

    @channel_shift.setter
    def channel_shift(self, value):
        self._channel_shift = self._validate_channel_shift(value)

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = value if value is not None else np.random.randint(0, 1000)

    @property
    def glitch_type(self):
        return self._glitch_type

    @glitch_type.setter
    def glitch_type(self, value):
        self._glitch_type = self._validate_glitch_type(value)

    @property
    def block_size(self):
        return self._block_size

    @block_size.setter
    def block_size(self, value):
        self._block_size = self._validate_block_size(value)

    def apply(self, image):
        """Apply glitch effect."""
        if image is None:
            raise ValueError("No image provided for processing")
        
        try:
            # Set random seed for reproducibility
            np.random.seed(self._seed)

            # Create a copy of the image
            glitched = image.copy()

            # Get image dimensions
            h, w = glitched.shape[:2]

            # Apply different glitch types based on selected type
            if self._glitch_type == 'random':
                # Random pixel modifications
                num_glitch_pixels = int(h * w * self._glitch_intensity)
                glitch_indices = np.random.randint(0, h*w, num_glitch_pixels)
                glitched.ravel()[glitch_indices] = np.random.randint(0, 256, num_glitch_pixels)

            elif self._glitch_type == 'block':
                # Block glitch effect
                num_blocks_h = h // self._block_size
                num_blocks_w = w // self._block_size

                for _ in range(int(num_blocks_h * num_blocks_w * self._glitch_intensity)):
                    block_x = np.random.randint(0, num_blocks_w)
                    block_y = np.random.randint(0, num_blocks_h)

                    start_x = block_x * self._block_size
                    start_y = block_y * self._block_size

                    # Shift or randomize block
                    block = glitched[
                        start_y:start_y+self._block_size, 
                        start_x:start_x+self._block_size
                    ]
                    
                    if np.random.random() < 0.5:
                        # Shift block
                        shift_x = np.random.randint(-self._channel_shift, self._channel_shift)
                        shift_y = np.random.randint(-self._channel_shift, self._channel_shift)
                        block = np.roll(block, (shift_y, shift_x), axis=(0, 1))
                    else:
                        # Randomize block
                        block[:] = np.random.randint(0, 256, block.shape)

                    glitched[
                        start_y:start_y+self._block_size, 
                        start_x:start_x+self._block_size
                    ] = block

            elif self._glitch_type == 'channel':
                # Channel shift glitch
                for channel in range(3):
                    shift = np.random.randint(-self._channel_shift, self._channel_shift)
                    channel_img = glitched[:,:,channel]
                    channel_img = np.roll(channel_img, shift, axis=0)
                    glitched[:,:,channel] = channel_img

            elif self._glitch_type == 'slice':
                # Image slice glitch
                slice_height = int(h * self._glitch_intensity)
                slice_y = np.random.randint(0, h - slice_height)
                
                # Shift or randomize slice
                slice_img = glitched[slice_y:slice_y+slice_height, :]
                if np.random.random() < 0.5:
                    shift_x = np.random.randint(-self._channel_shift, self._channel_shift)
                    slice_img = np.roll(slice_img, shift_x, axis=1)
                else:
                    slice_img = np.random.randint(0, 256, slice_img.shape)
                
                glitched[slice_y:slice_y+slice_height, :] = slice_img

            return glitched

        except Exception as e:
            raise RuntimeError(f"Error applying glitch effect: {str(e)}")

    def get_parameters(self):
        """Get current tool parameters."""
        return {
            "glitch_intensity": self._glitch_intensity,
            "channel_shift": self._channel_shift,
            "seed": self._seed,
            "glitch_type": self._glitch_type,
            "block_size": self._block_size
        }

    def update_parameters(self, params):
        """Update tool parameters."""
        if not isinstance(params, dict):
            raise ValueError("Parameters must be provided as a dictionary")
        
        if "glitch_intensity" in params:
            self.glitch_intensity = params["glitch_intensity"]
        if "channel_shift" in params:
            self.channel_shift = params["channel_shift"]
        if "seed" in params:
            self.seed = params["seed"]
        if "glitch_type" in params:
            self.glitch_type = params["glitch_type"]
        if "block_size" in params:
            self.block_size = params["block_size"]
    def get_valid_options(self):
        """Return valid options for parameters that require a drop-down menu."""
        return {
            "glitch_type": ['random', 'block', 'channel', 'slice']
        }