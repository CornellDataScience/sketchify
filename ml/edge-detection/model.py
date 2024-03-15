<<<<<<< HEAD
# from image_io import ImageIO
=======
>>>>>>> 9a4ee120ba02a05f92347a691fdeea7353d516ee
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

    image = np.array(Image.open(io.BytesIO(f)))

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


if __name__ == "__main__":
    with open("'../../public/Glazed-Donut.jpg'", 'rb') as f:
        r = f.read()

    edge_detection(r)
