import sys
import io
from PIL import Image
from image_segmentation.model import image_segmentation
from edge_detection.teed.model import edge_detection
from edge_smoothing.model import edge_smoothing
from convert_svg.model import convert_svg


image_bytes = sys.stdin.buffer.read()

# Converts bytes to a PIL image
image = Image.open(io.BytesIO(image_bytes))

# Crop coordinates from command line arguments
tl_x, tl_y, br_x, br_y = map(int, sys.argv[1:5])  

# Crop the image based on the provided coordinates
cropped_image = image.crop((tl_x, tl_y, br_x, br_y))

# Convert cropped image to bytes for further processing
cropped_bytes = io.BytesIO()
cropped_image.save(cropped_bytes, format='JPEG')
cropped_bytes = cropped_bytes.getvalue()

# Process the image
segmented_image = image_segmentation(cropped_bytes, (tl_x, tl_y), (br_x, br_y), "image_segmentation/sam_vit_h_4b8939.pth")
edged_image = edge_detection(segmented_image)
smoothed_image = edge_smoothing(edged_image)
svg = convert_svg(smoothed_image)

# Save the SVG output
output_path = '../public/output.svg'  # Adjust as necessary
with open(output_path, 'wb') as f:
    f.write(svg)