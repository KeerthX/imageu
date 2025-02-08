from PyQt5.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
    QRubberBand, QLabel, QWidget
)
from PyQt5.QtGui import QPixmap, QImage, QPainter, QCursor, QFont, QColor
from PyQt5.QtCore import Qt, QRectF, QPointF, QSizeF, QPoint, QRect, QTimer
import cv2
from .dialogs import AddProcessDialog, ConfigDialog

class ImageViewer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_variables()

    def setup_ui(self):
        # Setup scene with dark theme
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QColor("#1E1E1E"))
        self.setScene(self.scene)
        
        # Setup image item with improved rendering
        self.image_item = QGraphicsPixmapItem()
        self.image_item.setShapeMode(QGraphicsPixmapItem.BoundingRectShape)
        self.scene.addItem(self.image_item)
        
        # Enhanced view settings
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.setRenderHint(QPainter.TextAntialiasing, True)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        
        # Modern dark theme styling
        self.setStyleSheet("""
            QGraphicsView {
                background-color: #1E1E1E;
                border: none;
                selection-background-color: #264F78;
            }
            QScrollBar:horizontal {
                height: 12px;
                background: #1E1E1E;
                margin: 0px 20px 0px 20px;
            }
            QScrollBar:vertical {
                width: 12px;
                background: #1E1E1E;
                margin: 20px 0px 20px 0px;
            }
            QScrollBar::handle {
                background: #3E3E42;
                border-radius: 6px;
                min-height: 24px;
                min-width: 24px;
            }
            QScrollBar::handle:hover {
                background: #4E4E52;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background: none;
                border: none;
            }
            QScrollBar::add-page, QScrollBar::sub-page {
                background: none;
            }
        """)

        # Enhanced error label with modern styling
        self.error_label = QLabel(self)
        self.error_label.setFont(QFont("Segoe UI", 10))
        self.error_label.setStyleSheet("""
            QLabel {
                background-color: rgba(240, 52, 52, 0.95);
                color: #FFFFFF;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: 500;
                margin: 16px;
            }
        """)
        self.error_label.hide()

        # Set view background
        self.setBackgroundBrush(QColor("#1E1E1E"))
        
        # Enable mouse tracking for better interaction
        self.setMouseTracking(True)

    def setup_variables(self):
        self.original_image = None
        self.processed_image = None
        self.processing_stack = []
        self.zoom_factor = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 10.0
        self.error_state = False

    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.adjustSize()
        
        # Position error message at the bottom center
        label_x = (self.width() - self.error_label.width()) // 2
        label_y = self.height() - self.error_label.height() - 20
        
        # Add smooth fade-in animation effect
        self.error_label.setStyleSheet("""
            QLabel {
                background-color: rgba(240, 52, 52, 0.95);
                color: #FFFFFF;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: 500;
                margin: 16px;
                opacity: 1;
                transition: opacity 0.3s ease-in-out;
            }
        """)
        
        self.error_label.move(label_x, label_y)
        self.error_label.show()
        
        # Hide error message after delay with fade-out effect
        QTimer.singleShot(2800, lambda: self.error_label.setStyleSheet("""
            QLabel {
                background-color: rgba(240, 52, 52, 0.95);
                color: #FFFFFF;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: 500;
                margin: 16px;
                opacity: 0;
                transition: opacity 0.2s ease-in-out;
            }
        """))
        QTimer.singleShot(3000, self.error_label.hide)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self.zoom_factor *= factor
        else:
            factor = 0.8
            self.zoom_factor *= factor
        
        # Smooth zoom limits
        self.zoom_factor = max(self.min_zoom, min(self.zoom_factor, self.max_zoom))
        
        # Apply zoom with smooth transition
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.scale(factor, factor)
        
        # Update cursor based on zoom level
        if self.zoom_factor > 1.0:
            self.setCursor(QCursor(Qt.OpenHandCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))


    def load_image(self, file_path):
        try:
            image = cv2.imread(file_path)
            if image is None:
                raise ValueError("Failed to load image")
            
            self.original_image = image
            self.processed_image = image.copy()
            self.processing_stack = []
            self.update_display()
            self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
            self.zoom_factor = 1.0
            return True
            
        except Exception as e:
            self.show_error(f"Error loading image: {str(e)}")
            return False

    def update_display(self):
        if self.processed_image is None:
            return
        
        try:
            rgb_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
            height, width, channel = rgb_image.shape
            bytes_per_line = 3 * width
            
            qt_image = QImage(rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
            qt_pixmap = QPixmap.fromImage(qt_image)
            
            self.image_item.setPixmap(qt_pixmap)
            self.scene.setSceneRect(self.image_item.boundingRect())
            
        except Exception as e:
            self.show_error(f"Error updating display: {str(e)}")

    def add_processing(self, tool):
        if self.original_image is None:
            self.show_error("No image loaded")
            return False

        try:
            # Create a copy of the processing stack
            new_stack = self.processing_stack.copy()
            new_stack.append(tool)
            
            # Test the new processing chain
            temp_image = self.original_image.copy()
            for t in new_stack:
                temp_image = t.apply(temp_image)
            
            # If successful, update the actual stack and image
            self.processing_stack = new_stack
            self.processed_image = temp_image
            self.update_display()
            return True
            
        except Exception as e:
            self.show_error(f"Failed to add processing tool: {str(e)}")
            return False

    def remove_processing(self, index):
        try:
            if not 0 <= index < len(self.processing_stack):
                raise IndexError("Invalid processing tool index")
            
            # Create a copy of the processing stack without the removed tool
            new_stack = self.processing_stack[:index] + self.processing_stack[index+1:]
            
            # Test the new processing chain
            temp_image = self.original_image.copy()
            for tool in new_stack:
                temp_image = tool.apply(temp_image)
            
            # If successful, update the actual stack and image
            self.processing_stack = new_stack
            self.processed_image = temp_image
            self.update_display()
            return True
            
        except Exception as e:
            self.show_error(f"Failed to remove processing tool: {str(e)}")
            return False

    def move_processing(self, from_index, to_index):
        try:
            if not (0 <= from_index < len(self.processing_stack) and 
                   0 <= to_index < len(self.processing_stack)):
                raise IndexError("Invalid processing tool index")
            
            # Create a new processing stack with the moved tool
            new_stack = self.processing_stack.copy()
            tool = new_stack.pop(from_index)
            new_stack.insert(to_index, tool)
            
            # Test the new processing chain
            temp_image = self.original_image.copy()
            for tool in new_stack:
                temp_image = tool.apply(temp_image)
            
            # If successful, update the actual stack and image
            self.processing_stack = new_stack
            self.processed_image = temp_image
            self.update_display()
            return True
            
        except Exception as e:
            self.show_error(f"Failed to move processing tool: {str(e)}")
            return False

    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.adjustSize()
        self.error_label.move(10, self.height() - self.error_label.height() - 10)
        self.error_label.show()
        QTimer.singleShot(3000, self.error_label.hide)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self.zoom_factor *= factor
        else:
            factor = 0.8
            self.zoom_factor *= factor
        
        self.zoom_factor = max(self.min_zoom, min(self.zoom_factor, self.max_zoom))
        self.scale(factor, factor)

    def save_image(self, file_path):
        if self.processed_image is None:
            self.show_error("No image to save")
            return False
            
        try:
            cv2.imwrite(file_path, self.processed_image)
            return True
        except Exception as e:
            self.show_error(f"Error saving image: {str(e)}")
            return False

    def apply_processing(self):
        try:
            if self.original_image is None:
                raise ValueError("No image loaded")
            
            # Start with a fresh copy of the original image
            self.processed_image = self.original_image.copy()
        
            # Apply each tool in the processing stack
            for tool in self.processing_stack:
                self.processed_image = tool.apply(self.processed_image)
            
            # Update the display with the newly processed image
            self.update_display()
            return True
        
        except Exception as e:
            self.show_error(f"Error applying processing: {str(e)}")
            return False