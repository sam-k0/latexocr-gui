import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QTextEdit
from PySide6.QtGui import QPixmap, QImage
import numpy as np
from PySide6.QtCore import Qt
import ocr_requests as ocrr
import pyperclipimg as pcimg
import pyperclip as pc

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.TEMP_IMG_PATH = "temp.png"
        self.API_IMG_PREDICT = "http://127.0.0.1:8502/predict"


        self.setWindowTitle("PIL Image Viewer")
        self.setGeometry(100, 100, 500, 600)
        
        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Button
        self.button = QPushButton("Get Clipboard Image")
        self.button.clicked.connect(self.get_clipboard_image)
        layout.addWidget(self.button)
        
        # Image Views
        self.image_clipboard = QLabel()
        self.image_predicted = QLabel()
        self.image_clipboard.setFixedSize(400, 300) 
        self.image_predicted.setFixedSize(400,300)

        layout.addWidget(self.image_clipboard)
        layout.addWidget(QLabel(text="Converts to:"), alignment=Qt.AlignCenter)
        layout.addWidget(self.image_predicted)
        # text copy
        self.output_text = QTextEdit("This is a multi-line copyable text\nYou can copy me!")
        self.output_text.setReadOnly(True)  # Make it read-only
        layout.addWidget(self.output_text, alignment=Qt.AlignCenter)
        self.copy_output = QPushButton("Copy Output")
        self.copy_output.clicked.connect(self.set_clipboard_text)
        layout.addWidget(self.copy_output)
        
        self.setLayout(layout)
    
    ## Magic
    def get_clipboard_image(self):
        clip_img = pcimg.paste()
        if clip_img is None:
            # Show err as clipboard is empty / no image
            self.show_error("Invalid Clipboard", "The clipboard does not seem to contain any image data.")
            return

        self.set_pil_image(self.image_clipboard, clip_img)
        # Directly use the py lib to parse PIL img
        mathjax = ocrr.img2tex(clip_img)
        print(mathjax)
        # Render mathjax str to image
        math_plot = ocrr.latex2image(rf"""${mathjax}$""", image_name=None) # None wont save

        self.output_text.setText(mathjax)

        plot_img = ocrr.plot2pil(math_plot) # convert plot to pil image
        self.set_pil_image(self.image_predicted, plot_img)

    
    def set_pil_image(self, label, pil_image):
        # Convert PIL image to QPixmap
        image = pil_image.convert("RGBA")
        data = np.array(image)
        height, width, channel = data.shape
        bytes_per_line = channel * width
        q_image = QImage(data, width, height, bytes_per_line, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(q_image)
        
        # Set image to QLabel
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.setAlignment(Qt.AlignCenter)
    
    def show_error(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)  # Set error icon
        msg.setText(text)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()

    def set_clipboard_text(self):
        # get text from textfield and set to clipbaord
        pc.copy(self.output_text.toPlainText())
        
        print("Copied!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec())
