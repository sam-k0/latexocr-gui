from PIL import Image
from pix2tex.cli import LatexOCR
import pyperclip

img = Image.open('input/test.png')
model = LatexOCR()
print("--"*4)
print(model(img))
# Copy to clipboard
pyperclip.copy(model(img))

