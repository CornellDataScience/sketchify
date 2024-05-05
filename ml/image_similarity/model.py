from skimage.metrics import structural_similarity as ssim
import cv2
import numpy as np


def image_similarity(image1: bytes, image2: bytes) -> float:
    """
    Returns the similarity as a float score between two images using the Structural Similarity Index

    Args:
        image1: binary file representing the first image JPG or PNG
        image2: binary file representing the second image JPG or PNG

    Returns:
        A score representing how similar the two images are. 1.0 means that the two images are identical.
    """
    # Convert bytes to numpy array
    nparr1 = np.frombuffer(image1, np.uint8)
    nparr2 = np.frombuffer(image2, np.uint8)

    # Decode images
    # SSIM comparison is done on grayscale images
    image1 = cv2.imdecode(nparr1, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imdecode(nparr2, cv2.IMREAD_GRAYSCALE)

    # Ensure the images are the same size
    image1 = cv2.resize(image1, (256, 256))
    image2 = cv2.resize(image2, (256, 256))

    # Calculate the SSIM between the two images
    similarity_score, _ = ssim(image1, image2, full=True)

    return similarity_score
