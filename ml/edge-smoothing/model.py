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
    kernel_opening = np.ones((3, 3), np.uint8) 
    kernel_closing = np.ones((3, 3), np.uint8)

    img_inverted = cv2.bitwise_not(f)

    dst = cv2.fastNlMeansDenoising(img_inverted, 7, 15)

    i = 7
    j = 25
    h = 1
    while (h <= 45):
        dst = cv2.fastNlMeansDenoising(img_inverted, i, j, h)
        img_opening = opening(dst, kernel_opening, 1)
        img_closing = closing(img_opening, kernel_closing, 1)

        # Create the sharpening kernel 
        sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) 
  
        # Sharpen the image 
        sharpened_image = cv2.filter2D(img_closing, -1, sharpen_kernel) 

        #sharp = filters.unsharp_mask(img_closing, radius=1.5, amount=1.5, preserve_range=False)
        #sharp = (255*sharp).clip(0, 255).astype(np.uint8)

        plt.subplot(121),plt.imshow(sharpened_image,cmap = 'gray')
        plt.title("Image for " + str(i) + ", " + str(h)), plt.xticks([]), plt.yticks([])
        plt.show()
        h += 3
        #i += 7


    img_opening = opening(dst, kernel_opening, 1)
    img_closing = closing(img_opening, kernel_closing, 1)

    plt.subplot(121),plt.imshow(img_inverted,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    #plt.subplot(122),plt.imshow(img_closing,cmap = 'gray')
    #plt.title('Tweaked Image'), plt.xticks([]), plt.yticks([])

    plt.subplot(122),plt.imshow(img_closing,cmap = 'gray')
    plt.title('Denoised OG Image'), plt.xticks([]), plt.yticks([])

    plt.show()
    
    return f

def opening(img, kernel, iterations):
    img_erosion = cv2.erode(img, kernel, iterations=iterations) 
    return img_erosion

def closing(img, kernel, iterations):
    img_dilation = cv2.dilate(img, kernel, iterations=iterations) 
    return img_dilation

img = cv2.imread('../../public/canny_output.png', 0) 
edge_smoothing(img)
