from PIL import Image, ImageDraw
import io

def image_segmentation(f: bytes, tl: tuple[int, int], br: tuple[int, int]) -> bytes:
    """
    Convert a full-color image into a single mask based on the bounding boxes
    specified by tl and br.

    Args:
        f: binary file representing an image JPG or PNG
        tl: top-left coordinate of the bounding box mask
        br: bottom-right coordinate of the bounding box mask

    Returns:
        A binary file representing an image JPG or PNG
    """
    # Load the image from binary file
    image = Image.open(io.BytesIO(f))
    # Create a mask image of the same size, all pixels set to black
    mask = Image.new('L', image.size, 0)
    
    # Create a drawing context
    draw = ImageDraw.Draw(mask)
    # Draw a rectangle on the mask with white color (255)
    draw.rectangle([tl, br], fill=255)
    
    # Save the mask image to a binary format
    buffer = io.BytesIO()
    mask.save(buffer, format="PNG")
    return buffer.getvalue()
