import cv2


class FilterTool:
    def __init__(self):
        self.kernel_size = 5

    def apply(self, image):
        return cv2.GaussianBlur(image, (self.kernel_size, self.kernel_size), 0)

    def get_parameters(self):
        return {"kernel_size": self.kernel_size}
