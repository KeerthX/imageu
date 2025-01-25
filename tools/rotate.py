import cv2


class RotateTool:
    def __init__(self):
        self.angle = 90

    def apply(self, image):
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, self.angle, 1.0)
        return cv2.warpAffine(image, matrix, (w, h))

    def get_parameters(self):
        return {"angle": self.angle}
