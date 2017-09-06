import copy
import cv2
import numpy as np
from skimage import io, img_as_ubyte
from matplotlib import pyplot as plt
from skimage import measure
from scipy import ndimage
import argparse
import sys

class Segment:
    def __init__(self, segments=3):
        # define number of segments, with default 3
        self.segments = segments

    def kmeans(self, image):
        '''

        :param image: 2D or 3D image
        :return: segmented image same dims as original image (with n segments)
        '''
        image = cv2.GaussianBlur(image, (3,3), 0)
        if (len(image.shape) == 3):
            vectorized = image.reshape(-1, 3)
        else:
            vectorized = image.reshape(-1)

        vectorized = np.float32(vectorized)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, label, center = cv2.kmeans(vectorized, self.segments, None,
                                        criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        res = center[label.flatten()]
        segmented_image = res.reshape((image.shape))
        return label.reshape((image.shape[0], image.shape[1])),segmented_image.astype(np.uint8)

    def connectedComponent(self, binary_image, connectivity):
        '''

        :param binary_image:
        :param connectivity: 4 or 8
        :return: uint8 BW image of max area connected component
        TODO: extract top n-area
        '''
        uint8_img = np.uint8(binary_image)
        # Perform operation on binary image
        output = cv2.connectedComponentsWithStats(binary_image, connectivity, cv2.CV_32S)
        # Get the results
        num_labels = output[0]

        labels = output[1]
        # stat matrix
        stats = output[2]
        # centroid matrix
        centroids = output[3]

        fg_area = stats[1:, 4] # index 0 = background
        max_fg_area_index = np.argmax(fg_area)+1 # fg area indexs start with 1
        max_area_coordinate = stats[max_fg_area_index + 1, 0:4]
        max_fg_area = stats[max_fg_area_index + 1, 4]
        max_area_centroid = centroids[max_fg_area_index + 1]

        max_area_img = np.zeros(uint8_img.shape)
        max_area_img[labels == max_fg_area_index] = 255

        return np.uint8(max_area_img), num_labels, stats, max_fg_area_index

    def show_kmeans_regions(self, image, label_image):
        '''

        :param image:
        :param label_image: label array from kmeans function
        :return: uint8 image with dif grayscale value for each kmean region
        '''
        image_segmented = np.zeros(image.shape, dtype= np.uint8)
        num_segment = len(label_image)
        for i in range(num_segment):
            gray_level_increment = np.floor(255/num_segment)
            image_segmented[label_image == i] = i*gray_level_increment
        return image_segmented

    def extract_kmeans_binary(self, image, label_image, label):
        '''

        :param image:
        :param label_image: label array from kmeans function
        :param label: the label value (or specific kmean region) that we want to extract
        :return: uint8 image with choosen region set to white
        '''
        image_segmented = np.zeros(image.shape, dtype=np.uint8)
        image_segmented[label_image == label] = 255
        return image_segmented

    def thresholding(self, image, lower_val, upper_val):
        '''
        Do thresholding to extract pixels within range.
        Do image enhancement with closing, dilation and erosion

        TODO: add closing, dilation and erosion kernel size and iterations num

        :param image: grayscale 2 or 3-channel image
        :param lower_val: lower threshold value
        :param upper_val: upper threshold value
        :return: binary image (single channel)
        '''
        # 2 channel grayscale image copy
        img_copy = self.two_channel_grayscale(image)

        lower_mask = img_copy<lower_val
        img_copy[lower_mask] = 0
        self.disp_img_with_title(img_copy, "lower mask")

        upper_mask =img_copy>upper_val
        img_copy[upper_mask] =0
        self.disp_img_with_title(img_copy, "upper mask")

        # change to single channel
        unit8_img = img_as_ubyte(img_copy)
        ret, thresh = cv2.threshold(unit8_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self.disp_side_by_side(img_copy, thresh, 'after mask','theshold + ostu')

        #remove the inner holes
        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
                                   kernel=np.ones((2,2), np.uint8))
        self.disp_img_with_title(closing, 'closing')

        dilation = cv2.dilate(thresh, kernel=np.ones((2,2), np.uint8), iterations=1)
        self.disp_img_with_title(dilation, "dilation")

        erosion = cv2.erode(dilation, kernel=np.ones((2,2), np.uint8), iterations=1)
        self.disp_img_with_title(erosion, "erosion")
        return erosion

    def disp_side_by_side(self, image1, image2, label1, label2):
        titles = [label1, label2]
        images = [image1, image2]
        for i in range(2):
            plt.subplot(1, 2, i+1), plt.imshow(images[i], cmap = 'gray')
            plt.title(titles[i])
            plt.xticks([ ]), plt.yticks([])
        plt.show()

    def disp_img_with_title(self, image, title):
        plt.subplot(1, 1, 1), plt.imshow(image, cmap='gray')
        plt.title(title)
        plt.xticks([]), plt.yticks([])
        plt.show()

    def two_channel_grayscale(self, image):
        if (len(image.shape) ==3):
            img_copy = copy.copy(image)[:, :, 0]
        else:
            img_copy = copy.copy(image)
        return img_copy

    def laplacian(self, image):
        '''

        :param image: 2D or 3D gray image
        :return: uint8, 2D laplacian image
        '''
        img_1D = self.two_channel_grayscale(image)
        laplacian = cv2.Laplacian(img_1D, cv2.CV_64F)
        laplacian_abs = np.absolute(laplacian)
        laplacian_uint8 = np.uint8(laplacian_abs)
        return laplacian_uint8

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="Path to the image")
    ap.add_argument("-n", "--segments", required=False,
                    type=int, help="# of clusters")
    args = vars(ap.parse_args())

    image = cv2.imread(args["image"])

    if len(sys.argv) == 3:
        seg = Segment()
    else:
        seg = Segment(args["segments"])

    laplacian_uint8 = seg.laplacian(image)
    seg.disp_side_by_side(image, laplacian_uint8, "original image", "laplacian image")

    label, kmean_image = seg.kmeans(laplacian_uint8)
    seg.disp_side_by_side(laplacian_uint8, kmean_image, "laplacian image", "kmean_image")

    kmean_crystal_mask = seg.extract_kmeans_binary(image, label, 0)
    seg.disp_side_by_side(image, kmean_crystal_mask, "image", "kmean crystal mask")

    ret, thresh = cv2.threshold(laplacian_uint8, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    seg.disp_side_by_side(kmean_crystal_mask, thresh, "kmean crystal mask", "laplacian thresholding")