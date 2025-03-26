import requests
import json
import pyperclipimg as pcimg
import PIL
import matplotlib.pyplot as plt
import numpy as np
from pix2tex.cli import LatexOCR


TEMP_IMAGE_PATH_INPUT = 'input/temp_input.png'
TEMP_IMAGE_PATH_PREVIEW = 'input/temp_preview.png'
API_IMAGE_PREDICT = "http://127.0.0.1:8502/predict"
plt.rcParams["mathtext.fontset"] = "cm"  # Font changed to Computer Modern


#https://medium.com/@ealbanez/how-to-easily-convert-latex-to-images-with-python-9062184dc815
def latex2image(
    latex_expression, image_name, image_size_in=(3, 1), fontsize=16, dpi=200
):
    """
    A simple function to generate an image from a LaTeX language string.

    Parameters
    ----------
    latex_expression : str
        Equation in LaTeX markup language.
    image_name : str or path-like
        Full path or filename including filetype.
        Accepeted filetypes include: png, pdf, ps, eps and svg.
    image_size_in : tuple of float, optional
        Image size. Tuple which elements, in inches, are: (width_in, vertical_in).
    fontsize : float or str, optional
        Font size, that can be expressed as float or
        {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}.

    Returns
    -------
    fig : object
        Matplotlib figure object from the class: matplotlib.figure.Figure.

    """

    fig = plt.figure(figsize=image_size_in, dpi=dpi)
    text = fig.text(
        x=0.5,
        y=0.5,
        s=latex_expression,
        horizontalalignment="center",
        verticalalignment="center",
        fontsize=fontsize,
    )
    # Only save the figure if image_name is not None
    if image_name is not None:
        plt.savefig(image_name)

    return fig

# Convert a matplotlib plot to PIL Image
def plot2pil(plot):
    plot.canvas.draw()  # Ensure the canvas is drawn
    width, height = plot.canvas.get_width_height()

    # Get buffer in ARGB format
    buf = np.frombuffer(plot.canvas.buffer_rgba(), dtype=np.uint8)
    buf = buf.reshape((height, width, 4))  # Reshape to (H, W, 4) for ARGB

    # Convert ARGB to RGB (ignore the alpha channel)
    buf = buf[:, :, :3]

    return PIL.Image.fromarray(buf)

def img2tex(img):
    model = LatexOCR()
    return model(img)

if __name__ == "__main__":

    #result = latex2image(r"""$\underset{S}{\int\int}\ \vec{\nabla}\times\vec{B}\cdot d\vec{S}=\underset{C}{\oint}\ \vec{B}\cdot d\vec{l},$""", TEMP_IMAGE_PATH_PREVIEW)

    mathjax ="x=3\times4"
    # Ensure all backslashes are properly escaped
    mathjax_fixed = mathjax#.replace("\\", r"\\")


    result = latex2image(rf"""${repr(mathjax_fixed)[1:-1]}$""", None)
    plt.show() 

    newimg = plot2pil(result)
    print(newimg)
    newimg.show()

    exit()


    pil_img = pcimg.paste()
    if pil_img is None:
        print("No image found in clipboard")
        exit()

    pil_img.save(TEMP_IMAGE_PATH_INPUT)


    return_str = requests.post( 
        API_IMAGE_PREDICT,
        files={"file": open(TEMP_IMAGE_PATH_INPUT, "rb")}
    ).json()

    print(return_str)