from PyQt5.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QRubberBand, QLabel
)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QCursor
from PyQt5.QtCore import Qt, QRectF, QPointF, QSizeF, QPoint, QRect, QTimer
import cv2
import numpy as np

class ImageViewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.image_item = QGraphicsPixmapItem()
        self.scene.addItem(self.image_item)
        
        # Image storage
        self.original_image = None
        self.processed_image = None
        self.processing_stack = []
        
        # Zoom settings
        self.zoom_factor = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 10.0
        
        # Pan settings
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        
        # Selection box
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.is_selecting = False

        self.processing_stack = []
        self.original_image = None
        self.processed_image = None
        
        # Info label
        self.info_label = QLabel(self)
        self.info_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 180);
                color: white;
                padding: 5px;
                border-radius: 3px;
            }
        """)
        self.info_label.hide()

    def load_image(self, file_path):  # Changed from set_image to load_image
        try:
            # Read image using cv2
            self.original_image = cv2.imread(file_path)
            if self.original_image is None:
                raise ValueError("Failed to load image")
            
            self.processed_image = self.original_image.copy()
            self.update_display()
            self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
            self.zoom_factor = 1.0
            return True
        except Exception as e:
            print(f"Error loading image: {str(e)}")
            return False

    def update_display(self):  # Changed from update_image to update_display
        if self.processed_image is None:
            return
        
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
        
        height, width, channel = rgb_image.shape
        bytes_per_line = 3 * width
        
        qt_image = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        qt_pixmap = QPixmap.fromImage(qt_image)
        
        self.image_item.setPixmap(qt_pixmap)
        self.scene.setSceneRect(self.image_item.boundingRect())

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self.zoom_factor *= factor
        else:
            factor = 0.8
            self.zoom_factor *= factor
        
        # Ensure zoom stays within bounds
        self.zoom_factor = max(self.min_zoom, min(self.zoom_factor, self.max_zoom))
        
        # Apply zoom
        self.scale(factor, factor)
        
        # Update info label
        self.show_zoom_info()

    def show_zoom_info(self):
        self.info_label.setText(f"Zoom: {self.zoom_factor:.1f}x")
        self.info_label.adjustSize()
        self.info_label.move(10, 10)
        self.info_label.show()
        QTimer.singleShot(1500, self.info_label.hide)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.origin = event.pos()
            self.is_selecting = False
        elif event.button() == Qt.RightButton:
            self.setDragMode(QGraphicsView.NoDrag)
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()
            self.is_selecting = True
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.is_selecting:
            self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton and self.is_selecting:
            self.rubber_band.hide()
            self.is_selecting = False
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
            self.zoom_factor = 1.0
            self.show_zoom_info()
    def add_processing(self, tool):
        """Add a processing tool to the stack and apply it"""
        try:
            self.processing_stack.append(tool)
            self.apply_processing()
        except Exception as e:
            print(f"Error adding processing tool: {str(e)}")
            # Remove the tool if application failed
            self.processing_stack.pop()
            raise

    def apply_processing(self):
        """Apply all processing tools in the stack to the original image"""
        if self.original_image is None:
            return
        
        try:
            # Start with a fresh copy of the original image
            self.processed_image = self.original_image.copy()
            
            # Apply each tool in the stack sequentially
            for tool in self.processing_stack:
                self.processed_image = tool.apply(self.processed_image)
            
            # Update the display with the processed image
            self.update_display()
        except Exception as e:
            print(f"Error applying image processing: {str(e)}")
            raise

    def remove_processing(self, index):
        """Remove a processing tool and reapply remaining tools"""
        if 0 <= index < len(self.processing_stack):
            del self.processing_stack[index]
            self.apply_processing()

    def clear_processing(self):
        """Clear all processing tools and restore original image"""
        self.processing_stack.clear()
        if self.original_image is not None:
            self.processed_image = self.original_image.copy()
            self.update_display()

    def save_image(self, file_path):
        """Save the processed image to a file"""
        if self.processed_image is not None:
            try:
                cv2.imwrite(file_path, self.processed_image)
                return True
            except Exception as e:
                print(f"Error saving image: {str(e)}")
                return False
        return False

    def update_processing_order(self, new_stack):
        """Update the processing stack order and reapply"""
        self.processing_stack = new_stack
        self.apply_processing()