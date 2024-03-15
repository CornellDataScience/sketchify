from image_io import ImageIO

def edge_detection(f: bytes) -> bytes:
    """
    Converts a full-color image into an image with only the image edges

    Args:
        f: binary file representing an image JPG or PNG

    Returns:
        A binary file representing an image JPG or PNG
    """
    try:
        color_im = ImageIO.read_image(f)
    except FileNotFoundError:
        print(f"Error: File '{f}' not found in the current directory.")
        return

    gray_im = ImageIO.convert_grayscale(color_im)
    
