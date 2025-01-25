import cv2


class FilterTool:
    def __init__(self):
        self.kernel_size = 5  # Default kernel size (must be odd and > 0)

    def apply(self, image):
        # Ensure kernel size is odd and > 0
        if self.kernel_size <= 0 or self.kernel_size % 2 == 0:
            raise ValueError("Kernel size must be a positive odd integer.")
        return cv2.GaussianBlur(image, (self.kernel_size, self.kernel_size), 0)

    def get_parameters(self):
        return {"kernel_size": self.kernel_size}
