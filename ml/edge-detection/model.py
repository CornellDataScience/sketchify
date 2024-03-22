import io
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt


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
    edges = cv2.Canny(gray_image, 100, 200)
    is_success, im_buf_arr = cv2.imencode(".jpg", edges)
    byte_im = im_buf_arr.tobytes()

    return byte_im


# if __name__ == "__main__":
#     with open("../../public/Glazed-Donut.jpg", 'rb') as f:
#         r = f.read()

#     res = edge_detection(r)
#     image = np.array(Image.open(io.BytesIO(res)))

#     plt.imshow(image, cmap="gray")
#     plt.show()
