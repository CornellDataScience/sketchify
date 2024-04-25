import io
from PIL import Image
import cv2
import numpy as np
from .teed_model_main import teed_inference
import os


def edge_detection(f: bytes) -> bytes:
    """
    Converts a full-color image into an image with only the image edges

    Args:
        f: binary file representing an image JPG or PNG

    Returns:
        A binary file representing an image JPG or PNG
    """
    # Create a temporary file to write the input binary data (image)
    input_path = "edge_detection/teed/input/image.png"
    output_path = "edge_detection/teed/output/fused/image.png"
    with open(input_path, "wb") as file:
        file.write(f)

    # Run TEED inference
    teed_inference('edge_detection/teed/input')

    # Read the generated SVG data as binary
    with open(output_path, 'rb') as file:
        binary_data = file.read()

    image = np.array(Image.open(io.BytesIO(binary_data)))
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

    # Delete temporary files
    os.remove(input_path)
    os.remove(output_path)

    return binary_data, image
