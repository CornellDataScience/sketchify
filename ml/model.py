import sys
import io
from PIL import Image
from image_segmentation.model import image_segmentation
from edge_detection.model import edge_detection
from edge_smoothing.model import edge_smoothing
from convert_svg.model import convert_svg
import tempfile
import base64


def bytes_to_base64(byte_data):
    # Encode bytes as base64
    base64_string = base64.b64encode(byte_data)
    # Decode bytes to string
    base64_string = base64_string.decode('utf-8')
    return base64_string


if __name__ == "__main__":
    filepath = sys.argv[1]
    # print(filepath)
    with open(filepath, 'rb') as f:
        image_bytes = f.read()

    # # Converts bytes to a PIL image
    # image = Image.open(io.BytesIO(image_bytes))

    # Crop coordinates from command line arguments
    try:
        tl_x, tl_y, br_x, br_y = map(float, sys.argv[2:6])
        # Convert to int for pixels
        tl_x, tl_y, br_x, br_y = int(tl_x), int(tl_y), int(br_x), int(br_y)
    except ValueError as e:
        print(f"Error converting coordinates to integers: {e}")
        # sys.exit(1)

    # print(f"{tl_x} {tl_y} {br_x} {br_y}")

    # # Crop the image based on the provided coordinates
    # cropped_image = image.crop((tl_x, tl_y, br_x, br_y))

    # # Convert cropped image to bytes for further processing
    # cropped_bytes = io.BytesIO()
    # cropped_image.save(cropped_bytes, format='JPEG')
    # cropped_bytes = cropped_bytes.getvalue()

    # # Process the image
    segmented_image = image_segmentation(
        image_bytes, (tl_x, tl_y), (br_x, br_y), "image_segmentation/sam_vit_h_4b8939.pth")
    edged_image = edge_detection(segmented_image)
    smoothed_image = edge_smoothing(edged_image)
    svg = convert_svg(smoothed_image)

    # Save the SVG output
    # FOR DEBUGGING ONLY
    #
    # output_path = '../public/output-segmented.png'  # Adjust as necessary
    # with open(output_path, 'wb') as f:
    #     f.write(segmented_image)

    # output_path = '../public/output-edged.png'  # Adjust as necessary
    # with open(output_path, 'wb') as f:
    #     f.write(edged_image)

    # output_path = '../public/output-smoothed.png'  # Adjust as necessary
    # with open(output_path, 'wb') as f:
    #     f.write(smoothed_image)

    # output_path = '../public/output.svg'  # Adjust as necessary
    # with open(output_path, 'wb') as f:
    #     f.write(svg)

    # with tempfile.NamedTemporaryFile(delete=False, suffix='.svg') as f:
    #     f.write(svg)
    #     output_path = f.name

    result_base64 = bytes_to_base64(svg)
    print(result_base64)
