import copy
import cv2
import numpy as np
from skimage import img_as_ubyte
from matplotlib import pyplot as plt
from skimage import measure
from scipy import ndimage
import argparse
import sys

class Segment:
    def __init__(self):
        """"""
    def kmeans(self, image, segments):
        '''

        :param image: 2D or 3D image
        :return: segmented image same dims as original image (with n segments)
        '''
        image = cv2.GaussianBlur(image, (5,5), 0)
        if (len(image.shape) == 3):
            vectorized = image.reshape(-1, 3)
        else:
            vectorized = image.reshape(-1)

        vectorized = np.float32(vectorized)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, label, center = cv2.kmeans(vectorized, segments, None,
                                        criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        res = center[label.flatten()]
        segmented_image = res.reshape((image.shape))
        return label.reshape((image.shape[0], image.shape[1])),segmented_image.astype(np.uint8)

    def extract_top_area_components(self, binary_image, connectivity, num_of_crystal, label=None):
        '''

        :param binary_image:
        :param connectivity: 4 or 8
        :return: uint8 BW image of max area connected component
        TODO: extract top n-area
        '''
        uint8_img = np.uint8(binary_image)
        # Perform operation on binary image
        output = cv2.connectedComponentsWithStats(binary_image, labels=label, connectivity=connectivity, ltype=cv2.CV_32S)
        # Get the results
        num_labels = output[0]

        labels = output[1]
        # stat matrix
        stats = output[2]
        # centroid matrix
        centroids = output[3]

        fg_area = stats[1:, 4] # index 0 = background
        ascending_fg_index_arr = np.argsort(fg_area) # return the index arr of ascending crystal area
        sorted_fg_index_arr = np.flipud(ascending_fg_index_arr) # reverse the arr

        # Since here we skip the index 0 of background image, we need plus 1 to match the index here with the index of
        # the original labels array
        crystal_index_to_extract = sorted_fg_index_arr[0:num_of_crystal] + 1
        max_area_img = np.zeros(uint8_img.shape)
        for crystal_index in crystal_index_to_extract:
            max_area_img[labels == crystal_index] = 255

        # max_fg_area_index = np.argmax(fg_area)+1 # fg area indexs start with 1
        # max_area_coordinate = stats[max_fg_area_index, 0:4]
        # max_fg_area = stats[max_fg_area_index, 4]
        # max_area_centroid = centroids[max_fg_area_index]
        #
        # max_area_img = np.zeros(uint8_img.shape)
        # max_area_img[labels == max_fg_area_index] = 255

        # return np.uint8(max_area_img), num_labels, stats, max_fg_area_index
        return np.uint8(max_area_img)

    def kmeans_image(self, image, label_image, segments):
        '''

        :param image:
        :param label_image: label array from kmeans function
        :return: uint8 image with dif grayscale value for each kmean region
        '''
        image_segmented = np.zeros(image.shape, dtype= np.uint8)
        num_segment = segments
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

    def disp_multiple_image(self, image_arr, title_arr):
        for i in range(len(image_arr)):
            plt.subplot(3, np.floor(len(image_arr)/3), i+1), plt.imshow(image_arr[i], cmap="gray")
            plt.title(title_arr[i])
            plt.xticks([]), plt.yticks([])
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

    def laplacian(self, image, output_dim):
        '''

        :param image: 2D or 3D gray image
        :return: uint8, 2D/3D laplacian image
        '''
        if (output_dim==2):
            img = self.two_channel_grayscale(image)
        else:
            img = copy.copy(image)
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        laplacian_abs = np.absolute(laplacian)
        laplacian_uint8_filtered = np.uint8(laplacian_abs)
        return laplacian_uint8_filtered

    def various_closing(self, image, num_of_kernels, step_size, max_iteration):
        image_arr =[]
        title_arr = []
        for i in range(0, num_of_kernels):
            for j in range (max_iteration):
                kernel_size = (i + 1) * step_size
                closing_ij = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel=np.ones((kernel_size, kernel_size), np.uint8), iterations=(j+1))
                image_arr.append(closing_ij)
                title_ij = "kernel size " + str(kernel_size) + " iteration " + str(j+1)
                title_arr.append(title_ij)

        self.disp_multiple_image(image_arr, title_arr)
        return

    def various_opening(self, image, num_of_kernels, step_size, max_iteration):
        image_arr =[]
        title_arr = []
        for i in range(0, num_of_kernels):
            for j in range (max_iteration):
                kernel_size = (i + 1) * step_size
                opening_ij = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel=np.ones((kernel_size,kernel_size), np.uint8), iterations=(j+1))
                image_arr.append(opening_ij)
                title_ij = "kernel size " + str(kernel_size) + " iteration " + str(j+1)
                title_arr.append(title_ij)

        self.disp_multiple_image(image_arr, title_arr)
        return

    def various_erosion(self, image, num_of_kernels, step_size, max_iteration):
        image_arr = []
        title_arr = []
        for i in range(0, num_of_kernels):
            for j in range(max_iteration):
                kernel_size = (i + 1) * step_size
                erosion_ij = cv2.erode(image, kernel=np.ones((kernel_size,kernel_size), np.uint8), iterations=(j+1))
                image_arr.append(erosion_ij)
                title_ij = "kernel size " + str(kernel_size) + " iteration " + str(j + 1)
                title_arr.append(title_ij)

        self.disp_multiple_image(image_arr, title_arr)
        return

    def various_dilation(self, image, num_of_kernels, step_size, max_iteration):
        image_arr = []
        title_arr = []
        for i in range(0, num_of_kernels):
            for j in range(max_iteration):
                kernel_size = (i + 1) * step_size
                dilation_ij = cv2.dilate(image, kernel=np.ones((kernel_size,kernel_size), np.uint8), iterations=(j+1))
                image_arr.append(dilation_ij)
                title_ij = "kernel size " + str(kernel_size) + " iteration " + str(j + 1)
                title_arr.append(title_ij)

        self.disp_multiple_image(image_arr, title_arr)
        return

    def label_of_max_watershed_area(self, watershed_result_marker):
        vectorized_marker = watershed_result_marker.reshape(-1)
        unique, counts = np.unique(vectorized_marker, return_counts=True)
        print(np.asarray((unique, counts)).T)
        crystal_area_labels= unique[2:] #skip label -1 and 1
        crystal_areas = counts[2:]
        crystal_info = np.asarray((crystal_area_labels, crystal_areas)).T
        print(crystal_info)
        sorted_by_area = sorted(crystal_info, key=lambda tup: tup[1], reverse=True)
        print (sorted_by_area)
        print (sorted_by_area[0][0])
        return sorted_by_area[0][0]

class ProcessingFunction:
    def __init__(self):
        self.seg = Segment()

    def read_image(self, image_dir):
        image = cv2.imread(image_dir)
        return image

    def laplacian_func(self, current_image):
        return self.seg.laplacian(current_image, output_dim=2)

    def lower_thesholding(self, original_image, current_image, thresh_val):
        thresh_val = int(thresh_val)
        image_2D = self.seg.two_channel_grayscale(original_image)
        image_copy = copy.copy(current_image)
        image_copy[image_2D<thresh_val] = 255
        return image_copy

    def upper_thesholding(self, original_image, current_image, thresh_val):
        image_2D = self.seg.two_channel_grayscale(original_image)
        image_copy = copy.copy(current_image)
        image_copy[image_2D > thresh_val] = 255
        return image_copy

    def kmeans(self, current_image, segments):
        labels, result = self.seg.kmeans(current_image, segments)
        kmean_image = self.seg.kmeans_image(current_image, labels, segments)
        return kmean_image, labels

    def extract_crystal_mask(self, current_image, labels , user_chosen_label):
        return self.seg.extract_kmeans_binary(current_image, labels, user_chosen_label)

    def show_all_crystal(self, original_image, image_mask):
        mask = copy.copy(image_mask)
        mask = self.seg.two_channel_grayscale(mask)
        ret, markers2 = cv2.connectedComponents(mask)
        crystals_mask_kmean = np.zeros(original_image.shape, np.uint8)
        crystals_mask_kmean[markers2 > 0] = 255
        crystals_mask_kmean = np.uint8(crystals_mask_kmean)

        image_copy = copy.copy(original_image)
        image_copy[crystals_mask_kmean != 255] = 255
        return image_copy

    def show_top_area_crystals(self, original_image, image_mask, num_of_crystals):
        mask = copy.copy(image_mask)
        mask = self.seg.two_channel_grayscale(mask)
        max_area_crystal_kmean = self.seg.extract_top_area_components(mask, 8, num_of_crystals)
        biggest_crystal = copy.copy(original_image)
        biggest_crystal[max_area_crystal_kmean != 255] = 255
        return biggest_crystal

    # def show_all_crystal_larger_than(self, original_image, image_mask, ):

    def plot_histogram(self, image, image_mask):
        hist_with_mask = cv2.calcHist([image], [0], image_mask, [256], [0,256])
        # plt.plot(hist_mask)
        # plt.show()
        hist_y_axis = np.reshape(hist_with_mask, 256)
        hist_x_axis = np.arange(0,256) # create array of 0->255
        return hist_y_axis, hist_x_axis

    def closing(self, image, kernel_size, num_of_iter):
        return cv2.morphologyEx(image, cv2.MORPH_CLOSE,
                                 kernel=np.ones((kernel_size, kernel_size), np.uint8), iterations=num_of_iter)

    def opening(self, image, kernel_size, num_of_iter):
        return cv2.morphologyEx(image, cv2.MORPH_OPEN,
                                kernel=np.ones((kernel_size,kernel_size), np.uint8), iterations=num_of_iter)

    def erosion(self, image, kernel_size, num_of_iter):
        return cv2.erode(image, kernel=np.ones((kernel_size,kernel_size), np.uint8), iterations=num_of_iter)


    def dilation(self, image, kernel_size, num_of_iter):
        return cv2.dilate(image, kernel=np.ones((kernel_size,kernel_size), np.uint8), iterations=num_of_iter)
