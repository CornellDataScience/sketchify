from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
import torch
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import sys
import io
from PIL import Image
# sys.path.append("..")  # Ensure the path includes 'segment_anything' module
from os import path
path_to_checkpoint = path.abspath(
    path.join(path.dirname(__file__), 'sam_vit_b_01ec64.pth'))


def image_segmentation(f: bytes, tl: tuple[int, int], br: tuple[int, int], checkpoint=path_to_checkpoint) -> bytes:
    """
    Segment a specific area of the image defined by the bounding box coordinates.

    Args:
        f: binary file representing an image JPG or PNG.
        tl: top-left coordinate of the bounding box (x,y).
        br: bottom-right coordinate of the bounding box (x,y).
        checkpoint: the path to the model checkpoint

    Returns:
        A binary file representing the segmented area of the image in JPG or PNG format.
    """
    # Define vars for SegmentAnything
    model_type = "vit_b"
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    sam = sam_model_registry[model_type](
        checkpoint=checkpoint).to(device=device)

    # Convert bytes data to an image
    image_stream = io.BytesIO(f)
    image = Image.open(image_stream).convert('RGB')
    image_np = np.array(image)

    # Convert colors from RGB to BGR format used by OpenCV
    image_bgr = cv.cvtColor(image_np, cv.COLOR_RGB2BGR)
    image_rgb = cv.cvtColor(image_bgr, cv.COLOR_BGR2RGB)

    # Initialize the predictor
    predictor = SamPredictor(sam)
    predictor.set_image(image_rgb)

    # Define the bounding box
    box = np.array([tl[0], tl[1], br[0], br[1]])

    # Generate masks within the defined bounding box
    masks, scores, logits = predictor.predict(box=box, multimask_output=True)

    # Combine masks and original image
    if masks.any():  # Check if any mask was generated
        segmentation_mask = masks[0]  # Use the first mask
        for i in range(1, len(masks)):
            segmentation_mask = segmentation_mask | masks[i]  # Combine masks
        # Apply the combined mask to the original image
        segmented_img = (
            segmentation_mask[..., None] * image_rgb).astype(np.uint8)
    else:
        segmented_img = np.zeros_like(image_rgb)

    # Convert numpy array back to PIL Image
    segmented_img_pil = Image.fromarray(
        cv.cvtColor(segmented_img, cv.COLOR_RGB2BGR))

    # Save the segmented image to bytes
    img_byte_arr = io.BytesIO()
    # You can change 'PNG' to 'JPEG' if you prefer
    segmented_img_pil.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr
