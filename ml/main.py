from image_segmentation.model import image_segmentation
from ml.edge_detection.teed.model import edge_detection
from edge_smoothing.model import edge_smoothing
from convert_svg.model import convert_svg

# Load
image_path = '../public/bear_fishing.jpg'
with open(image_path, 'rb') as f:
    image_bytes = f.read()

# Hardcoded for now
tl = (1142, 134)  # Top-left corner of the image (adjust based on your image)
br = (1739, 1064)  # Bottom-right corner of the image (adjust based on your image)

segmented_image = image_segmentation(
    image_bytes, tl, br, "image_segmentation/sam_vit_h_4b8939.pth")
edged_image = edge_detection(segmented_image)
smoothed_image = edge_smoothing(edged_image)
svg = convert_svg(smoothed_image)

# Save
segmented_image_path = '../public/bear_fishing_output.svg'
with open(segmented_image_path, 'wb') as f:
    f.write(svg)
