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
    segmented_image = image_segmentation(
        image_bytes, tl, br, "image_segmentation/sam_vit_h_4b8939.pth")

    # Process Image
    edged_image = edge_detection(segmented_image)
    smoothed_image = edge_smoothing(edged_image)
    svg = convert_svg(smoothed_image)

    segmented_image_path = "../public/output.svg"

    with open(segmented_image_path, 'wb') as f:
        f.write(svg)

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
    i = convertImage(img_path)
    b = compareImages(i, sketch_path)
    # with open('finish.txt', 'wb') as fh:
    # fh.write(str(b)+'\n')
    return str(b)


if __name__ == "__main__":
    similarity = main(sys.argv[1], sys.argv[2])
    print(similarity)
