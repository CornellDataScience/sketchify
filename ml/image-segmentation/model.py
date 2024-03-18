import torch
import torchvision
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import sys
import io
from PIL import Image
sys.path.append("..")  # Ensure the path includes 'segment_anything' module
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor


sam = sam_model_registry["default"](checkpoint="sam_vit_h_4b8939.pth")
checkpoint = "sam_vit_h_4b8939.pth"
model_type = "vit_h"
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
sam = sam_model_registry[model_type](checkpoint=checkpoint).to(device = device)
mask_generator = SamAutomaticMaskGenerator(sam)
predictor = SamPredictor(sam)

mask_generator = SamAutomaticMaskGenerator(sam)

image_bgr = cv.imread('../../public/Glazed-Donut.jpg')
image_rgb = cv.cvtColor(image_bgr, cv.COLOR_BGR2RGB)

sam_result = mask_generator.generate(image_rgb)

def image_segmentation(f: bytes, tl: tuple[int, int], br: tuple[int, int]) -> bytes:
    """
    Segment a specific area of the image defined by the bounding box coordinates.
    
    Args:
        f: binary file representing an image JPG or PNG.
        tl: top-left coordinate of the bounding box (x,y).
        br: bottom-right coordinate of the bounding box (x,y).
        
    Returns:
        A binary file representing the segmented area of the image in JPG or PNG format.
    """
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
        segmented_img = (segmentation_mask[..., None] * image_rgb).astype(np.uint8)
    else:
        segmented_img = np.zeros_like(image_rgb)

    # Convert numpy array back to PIL Image
    segmented_img_pil = Image.fromarray(cv.cvtColor(segmented_img, cv.COLOR_RGB2BGR))
    
    # Save the segmented image to bytes
    img_byte_arr = io.BytesIO()
    segmented_img_pil.save(img_byte_arr, format='PNG')  # You can change 'PNG' to 'JPEG' if you prefer
    img_byte_arr = img_byte_arr.getvalue()
    
    return img_byte_arr

# First, let's read the image file and convert it to bytes
doughnut_image_path = '../../public/Glazed-Donut.jpg'  # Adjust the path to where your image is stored
with open(doughnut_image_path, 'rb') as f:
    doughnut_bytes = f.read()

# Define the bounding box coordinates (top-left and bottom-right)
# Here, I'm assuming you want to segment the whole image
# But you can adjust these coordinates based on the doughnut's position in your image
tl = (0, 0)  # Top-left corner of the image (adjust based on your image)
br = (1200, 1200)  # Bottom-right corner of the image (adjust based on your image)

# Now, let's segment the image
segmented_image_bytes = image_segmentation(doughnut_bytes, tl, br)

# Display the mask
image = np.array(Image.open(io.BytesIO(segmented_image_bytes)))
plt.imshow(image)
plt.axis('off')
plt.show()

# Finally, let's save the segmented image to a new file so we can view it
segmented_image_path = 'Segmented-Glazed-Donut.png'
with open(segmented_image_path, 'wb') as f:
    f.write(segmented_image_bytes)