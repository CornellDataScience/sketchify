# from image_segmentation.model import image_segmentation
# from edge_detection.teed.model import edge_detection
# from edge_smoothing.model import edge_smoothing
# from convert_svg.model import convert_svg


# # Load
# image_path = '../public/bear_fishing.jpg'
# with open(image_path, 'rb') as f:
#     image_bytes = f.read()

# # Hardcoded for now
# tl = (1142, 134)  # Top-left corner of the image (adjust based on your image)
# br = (1739, 1064)  # Bottom-right corner of the image (adjust based on your image)

# segmented_image = image_segmentation(
#     image_bytes, tl, br, "image_segmentation/sam_vit_h_4b8939.pth")
# edged_image = edge_detection(segmented_image)
# smoothed_image = edge_smoothing(edged_image)
# svg = convert_svg(smoothed_image)

# # Save
# segmented_image_path = '../public/bear_fishing_output.svg'
# with open(segmented_image_path, 'wb') as f:
#     f.write(svg)

from image_segmentation.model import image_segmentation
from edge_detection.model import edge_detection
from edge_smoothing.model import edge_smoothing
from convert_svg.model import convert_svg
from image_similarity.model import image_similarity
import sys
import tempfile
import os
import base64


def bytes_to_base64(byte_data):
    # Encode bytes as base64
    base64_string = base64.b64encode(byte_data)
    # Decode bytes to string
    base64_string = base64_string.decode('utf-8')
    return base64_string


def convertImage(filepath: str) -> str:
    """
    Processes the image at the location "filepath" and converts it into an svg sketch.
    Returns the filepath of said svg sketch.
    """
    with open(filepath, 'rb') as f:
        image_bytes = f.read()

    # Image Segmentation not yet implemented in frontend
    # Hardcoded for now
    tl = (1142, 134)  # Top-left corner of the image (adjust based on your image)
    # Bottom-right corner of the image (adjust based on your image)
    br = (1739, 1064)
    segmented_image = image_segmentation(image_bytes, tl, br)

    # Process Image
    edged_image = edge_detection(segmented_image)
    smoothed_image = edge_smoothing(edged_image)

    # segmented_image_path = "../public/output.svg"

    # Create a temporary file to write the input binary data (image)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as f:
        f.write(smoothed_image)
        segmented_image_path = f.name

    return segmented_image_path


def compareImages(filePath1: str, filePath2: str) -> float:
    """
    Processes the similarity score of the images located at "filePath1" and "filePath2".
    Returns said similarity score.
    """
    with open(filePath1, 'rb') as file1:
        image1 = file1.read()
    with open(filePath2, 'rb') as file2:
        image2 = file2.read()

    return image_similarity(image1, image2)


def main(img_path: str, sketch_path: str):
    """
    Parsing the arguments passed into the script
    """
    # parser = argparse.ArgumentParser(description='Short sample app')
    # parser.add_argument('image filepath')
    # parser.add_argument('sketch filepath')
    # args = parser.parse_args()

    # Runs the two functions above, saving the result svg into output.svg.
    # The similarity score is saved into finish.txt.
    full_image_to_sketch = convertImage(img_path)
    similarity = compareImages(full_image_to_sketch, sketch_path)
    os.remove(full_image_to_sketch)
    # with open('finish.txt', 'wb') as fh:
    # fh.write(str(b)+'\n')
    return str(similarity)


def run_ml_model(filepath: str, tl_x: str, tl_y: str, br_x: str, br_y: str):
    # print(filepath)
    with open(filepath, 'rb') as f:
        image_bytes = f.read()

    # # Converts bytes to a PIL image
    # image = Image.open(io.BytesIO(image_bytes))

    # Crop coordinates from command line arguments
    try:
        # tl_x, tl_y, br_x, br_y = map(float, sys.argv[2:6])
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
        image_bytes, (tl_x, tl_y), (br_x, br_y))
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
    return result_base64


if __name__ == "__main__":
    # See if we should run image_similarity or run the model
    task = sys.argv[1]
    if sys.argv[1] == "similarity":
        similarity = main(sys.argv[2], sys.argv[3])
        print(similarity)
    elif sys.argv[1] == "model":
        filepath = sys.argv[2]
        tl_x, tl_y, br_x, br_y = map(float, sys.argv[3:7])
        resull_base64 = run_ml_model(filepath, tl_x, tl_y, br_x, br_y)
        print(resull_base64)
