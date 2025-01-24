import cv2

class FilterTool:
    def __init__(self):
        self.kernel_size = 5

    def configure(self):
        print("Configure Filter: (Example: kernel_size=5)")

    def apply(self, image):
        return cv2.GaussianBlur(image, (self.kernel_size, self.kernel_size), 0)
