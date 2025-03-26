import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QPixmap, QImage
from PIL import Image
import numpy as np
from PySide6.QtCore import Qt
import ocr_requests as ocrr

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PIL Image Viewer")
        self.setGeometry(100, 100, 500, 600)
        
        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Button
        self.button = QPushButton("Get Clipboard Image")
        self.button.clicked.connect(self.load_image)
        layout.addWidget(self.button)
        
        # Image Views
        self.image_label1 = QLabel()
        self.image_label2 = QLabel()
        layout.addWidget(self.image_label1)
        layout.addWidget(QLabel(text="Converts to:"), alignment=Qt.AlignCenter)
        layout.addWidget(self.image_label2)
        
        self.setLayout(layout)
    
    def get_clipboard_image(self):
        image = Image.open("input/temp.png")  # Replace with your image path
        self.set_pil_image(self.image_label1, image)
        self.set_pil_image(self.image_label2, image)
    
    def set_pil_image(self, label, pil_image):
        # Convert PIL image to QPixmap
        image = pil_image.convert("RGBA")
        data = np.array(image)
        height, width, channel = data.shape
        bytes_per_line = channel * width
        q_image = QImage(data, width, height, bytes_per_line, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(q_image)
        
        # Set image to QLabel
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec())
