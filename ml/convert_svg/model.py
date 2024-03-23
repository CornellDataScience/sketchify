import tempfile
import os
import vtracer
from PIL import Image
import numpy as np


def convert_svg(f: bytes) -> bytes:
    """
    Converts a monochrome JPG/PNG file into an SVG

    Args:
        f: binary file representing an image JPG or PNG

    Returns:
        A binary file representing an SVG
    """

    # Create a temporary file to write the input binary data (image)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_input:
        tmp_input.write(f)
        tmp_input_path = tmp_input.name

    # Define the output path for the SVG file
    output_path = "../../ml/convert-svg/output.svg"

    # Call the vtracer library to convert the temporary file to SVG
    vtracer.convert_image_to_svg_py(tmp_input_path,
                                    output_path,
                                    colormode='binary'
                                    )

    # Read the generated SVG data as binary
    with open(output_path, 'rb') as file:
        binary_data = file.read()

    # Delete temporary files
    os.remove(tmp_input_path)
    os.remove(output_path)

    return binary_data
