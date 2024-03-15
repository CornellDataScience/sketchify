import matplotlib.pyplot as plt
import numpy as np


class ImageIO:

    def read_im(file):
        image = plt.imread(file)
        return image
    
    def convert_grayscale(im):
        return np.dot(im[..., :3], [0.299, 0.587, 0.114])
    
    def display_image(im, title):

        plt.imshow(im)
        plt.title(title)
        plt.show()
    
