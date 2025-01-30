import cv2

class FilterTool:
    def __init__(self):
        self.kernel_size = 5  # Default kernel size (must be odd and > 0)

    def apply(self, image):
        # Ensure kernel size is odd and > 0
        if self.kernel_size <= 0:
            raise ValueError("Filter size must be greater than 0.")
        if self.kernel_size % 2 == 0:
            raise ValueError("Filter size must be an odd number (e.g., 3, 5, 7).")

        try:
            return cv2.GaussianBlur(image, (self.kernel_size, self.kernel_size), 0)
        except cv2.error as e:
            raise RuntimeError(f"OpenCV error in FilterTool: {str(e)}")

    def get_parameters(self):
        return {"kernel_size": self.kernel_size}
