# LaTeX-OCR GUI

A quack (🦆) and dirty implementation of a gui app based on [LaTeX-OCR](https://github.com/lukas-blecher/LaTeX-OCR).

Follows a simple workflow:

1. Copy an image containg a mathjax / latex math figure
2. Paste it into the app
3. Compare the original figure to the displayed predicted figure
4. If it seems good, copy the mathjax text from the textfield

## Installing

- Follow the setup guide from LaTeX-OCR
- Additional modules are `pyside6`, `pyperclipimg` and `numpy`?
- Tested using Python/conda 3.11.11