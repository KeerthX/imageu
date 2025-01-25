from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage
import cv2


class ImageViewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.image_item = QGraphicsPixmapItem()
        self.scene.addItem(self.image_item)
        self.original_image = None
        self.processed_image = None
        self.processing_stack = []

    def set_image(self, file_path):
        self.original_image = cv2.imread(file_path)
        self.processed_image = self.original_image.copy()
        self.update_image()

    def add_processing(self, tool):
        self.processing_stack.append(tool)
        self.apply_processing()

    def apply_processing(self):
        if self.original_image is None:
            return
        image = self.original_image.copy()
        for tool in self.processing_stack:
            image = tool.apply(image)
        self.processed_image = image
        self.update_image()

    def update_image(self):
        if self.processed_image is None:
            return
        height, width, channel = self.processed_image.shape
        bytes_per_line = 3 * width
        qt_image = QImage(self.processed_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        qt_pixmap = QPixmap.fromImage(qt_image.rgbSwapped())
        self.image_item.setPixmap(qt_pixmap)

    def save_image(self, file_path):
        cv2.imwrite(file_path, self.processed_image)
