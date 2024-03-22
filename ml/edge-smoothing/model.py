import cv2
import numpy as np
import PIL as pil
from matplotlib import pyplot as plt
import skimage.filters as filters

def edge_smoothing(f: bytes) -> bytes:
    """
    Converts an edge detection output into a coloring book outline, including
    all necessary postprocessing

    Args:
        f: binary file representing an image JPG or PNG

    Returns:
        A binary file representing an image JPG or PNG
    """

    kernel_opening = (3, 3)
    kernel_closing = (3, 3)

    # Prepare the image to be contoured
    prepared_img = contour_preparation(f)
    denoised_img = denoising(prepared_img)

    # Contour the image
    contours = contour_image(denoised_img)

    # Enhance the image for plotting preparation
    # Create an empty image to draw filtered contours
    filtered_image = np.zeros_like(img)

    # Draw the filtered contours on the empty image
    new_image = cv2.drawContours(filtered_image, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    # Close all of the edges
    closed_img = closing(new_image, kernel_closing, 2)

    # Invert the image
    inverted_img = cv2.bitwise_not(closed_img)

    # Display the original and enhanced image
    display(f, inverted_img)

    return inverted_img

# method to execute opening (gaps become larger). the kernel size and iteration amount affects how much opening occurs
def opening(img, kernel, iterations):
    """
    Erodes an image

    Args:
        img: binary file representing an image JPG or PNG
        kernel: a tuple representing a valid kernel value
        iterations: the number of times the image is to be eroded

    Returns:
        A binary file representing an image JPG or PNG
    """

    img_erosion = cv2.erode(img, kernel, iterations=iterations)
    #img_dilation = cv2.dilate(img_erosion, kernel, iterations=iterations)
    return img_erosion

# method to execute closing (gaps become smaller). the kernel size and iteration amount affects how much closing occurs
def closing(img, kernel, iterations):
    """
    Closes any gaps in the image edges

    Args:
        img: binary file representing an image JPG or PNG
        kernel: a tuple representing a valid kernel value
        iterations: the number of times to apply closing on the image

    Returns:
        A binary file representing an image JPG or PNG
    """

    closed_img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=1)
    img_dilation = cv2.dilate(closed_img, kernel, iterations=iterations)
    #img_erosion = cv2.erode(img_dilation, kernel, iterations=iterations)
    return img_dilation

# Prepare the image to extract the contours
def contour_preparation(img):
    """
    Prepares the image for contour extraction

    Args:
        img: binary file representing an image JPG or PNG

    Returns:
        A binary file representing an image JPG or PNG
    """

    # Dilate the edges before denoising
    # Necessary to prevent thin prominent lines from weathering away
    dilated_edges = cv2.dilate(img, (3,3), iterations=1)

    # Denoising the image
    dst = cv2.fastNlMeansDenoising(dilated_edges, 11, 21, 25)

    # Setting a threshold for contour finding
    # Getting all colored pixels and setting them to white if above the threshold
    ret, thresh = cv2.threshold(dst, 120, 255, cv2.THRESH_BINARY)

    return thresh

# Contour the image and extract only the prominent contours
def contour_image(img):
    """
    Contours the image and only extracts the relevant contours

    Args:
        img: binary file representing an image JPG or PNG

    Returns:
        A binary file representing an image JPG or PNG
    """

    # Extracting the contours of the image
    contours, hierarchy = cv2.findContours(img,
    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Establish a threshold for the minimum area of a contour
    min_area_threshold = 10

    # Filter out the contours with small area
    filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > min_area_threshold]

    return filtered_contours

# method to denoise the image, removing excess dots
def denoising(img):
    """
    Denoises an image by removing any pixels that aren't a black color.
    The image is sharpened after denoising.

    Args:
        img: binary file representing an image JPG or PNG

    Returns:
        A binary file representing an image JPG or PNG
    """

    dst = cv2.fastNlMeansDenoising(img, None, 11, 25, 43)

    for i in dst:
        for a in range(len(i)):
            if i[a]<=70:
                i[a] = 0
    # Create the sharpening kernel
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

    # Sharpen the image
    sharpened_image = cv2.filter2D(dst, -1, sharpen_kernel)

    return sharpened_image

# method to display the output image
def display(img_og, img_new):
    """
    Graphs and displays the original image and the altered image

    Args:
        img_og: binary file representing the original JPG or PNG image
        img_new: binary file representing the altered JPG or PNG image

    Returns:
        A binary file representing an image JPG or PNG
    """

    plt.subplot(121),plt.imshow(img_og,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img_new,cmap = 'gray')
    plt.title('Altered Image'), plt.xticks([]), plt.yticks([])
    plt.show()

# Run the edge smoothing function on an image
img = cv2.imread('../../public/canny_output.png', 0)
edge_smoothing(img)
