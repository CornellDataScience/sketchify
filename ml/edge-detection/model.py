# from image_io import ImageIO
import io
from PIL import Image
import cv2
import numpy as np


def edge_detection(f: bytes) -> bytes:
    """
    Converts a full-color image into an image with only the image edges

    Args:
        f: binary file representing an image JPG or PNG

    Returns:
        A binary file representing an image JPG or PNG
    """
    # try:
    #     color_im = ImageIO.read_image(f)
    # except FileNotFoundError:
    #     print(f"Error: File '{f}' not found in the current directory.")
    #     return

    # gray_im = ImageIO.convert_grayscale(color_im)

    image = np.array(Image.open(io.BytesIO(f)))

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


if __name__ == "__main__":
    with open("'../../public/Glazed-Donut.jpg'", 'rb') as f:
        r = f.read()

    edge_detection(r)
