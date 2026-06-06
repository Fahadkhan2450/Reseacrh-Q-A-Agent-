import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QWidget, QLabel, QFileDialog)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class ImageProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sleek Image Processing App")
        self.setGeometry(100, 100, 900, 700)

        # Variables to store images
        self.original_image = None
        self.processed_image = None

        self.initUI()

    def initUI(self):
        # Main Layout Container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Image Display Area (Live Preview)
        self.image_label = QLabel("No Image Loaded")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px dashed #aaa; background-color: #f0f0f0;")
        # This ensures the image stays within the UI bounds (Feature 6)
        self.image_label.setMinimumSize(400, 400)
        main_layout.addWidget(self.image_label)

        # Button Layout
        btn_layout = QHBoxLayout()
        
        # Creating Buttons
        btn_open = QPushButton("📂 Open Image")
        btn_gray = QPushButton("🎨 Grayscale")
        btn_blur = QPushButton("🌀 Blur")
        btn_edge = QPushButton("🔍 Edge Detection")
        btn_save = QPushButton("💾 Save Image")

        # Connect Buttons to Functions
        btn_open.clicked.connect(self.open_image)
        btn_gray.clicked.connect(self.to_grayscale)
        btn_blur.clicked.connect(self.apply_blur)
        btn_edge.clicked.connect(self.edge_detection)
        btn_save.clicked.connect(self.save_image)

        # Add buttons to layout
        for btn in [btn_open, btn_gray, btn_blur, btn_edge, btn_save]:
            btn_layout.addWidget(btn)
            btn.setHeight = 40

        main_layout.addLayout(btn_layout)

    def display_image(self, img):
        """Converts OpenCV BGR image to PyQt QPixmap and displays it."""
        if img is None:
            return

        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Get dimensions
        height, width, channel = img_rgb.shape
        bytes_per_line = 3 * width
        
        # Create QImage and then QPixmap
        q_img = QImage(img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        
        # Scale pixmap to fit label while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), 
                                      Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.image_label.setPixmap(scaled_pixmap)

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.processed_image = self.original_image.copy()
            self.display_image(self.processed_image)

    def to_grayscale(self):
        if self.original_image is not None:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            # Convert back to 3-channel BGR so display logic remains consistent
            self.processed_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            self.display_image(self.processed_image)

    def apply_blur(self):
        if self.original_image is not None:
            self.processed_image = cv2.GaussianBlur(self.original_image, (15, 15), 0)
            self.display_image(self.processed_image)

    def edge_detection(self):
        if self.original_image is not None:
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            self.processed_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            self.display_image(self.processed_image)

    def save_image(self):
        if self.processed_image is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG (*.png);;JPEG (*.jpg)")
            if file_path:
                cv2.imwrite(file_path, self.processed_image)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessorApp()
    window.show()
    sys.exit(app.exec_())
