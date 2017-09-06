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
        image = cv2.GaussianBlur(image, (5,5), 0)
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

    def extract_connected_component(self, binary_image, connectivity, label=None):
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
        max_fg_area_index = np.argmax(fg_area)+1 # fg area indexs start with 1
        max_area_coordinate = stats[max_fg_area_index + 1, 0:4]
        max_fg_area = stats[max_fg_area_index + 1, 4]
        max_area_centroid = centroids[max_fg_area_index + 1]

        max_area_img = np.zeros(uint8_img.shape)
        max_area_img[labels == max_fg_area_index] = 255

        # return np.uint8(max_area_img), num_labels, stats, max_fg_area_index
        return np.uint8(max_area_img)

    def kmeans_image(self, image, label_image):
        '''

        :param image:
        :param label_image: label array from kmeans function
        :return: uint8 image with dif grayscale value for each kmean region
        '''
        image_segmented = np.zeros(image.shape, dtype= np.uint8)
        num_segment = self.segments
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

    laplacian_2D= seg.laplacian(image, output_dim=2)
    seg.disp_side_by_side(image, laplacian_2D, "original image", "laplacian image")

    image_2D = seg.two_channel_grayscale(image)
    laplacian_uint8_filtered = copy.copy(laplacian_2D)
    laplacian_uint8_filtered[image_2D<50] = 255
    laplacian_uint8_filtered[image_2D>150] =255
    seg.disp_side_by_side(laplacian_2D, laplacian_uint8_filtered, "laplacian image", "laplacian image filtered")

    label, result = seg.kmeans(laplacian_uint8_filtered)
    kmean_image = seg.kmeans_image(laplacian_uint8_filtered, label)
    seg.disp_side_by_side(laplacian_uint8_filtered, kmean_image, "laplacian image", "kmean_image")

    kmean_crystal_mask = seg.extract_kmeans_binary(kmean_image, label, 4)
    seg.disp_side_by_side(image, kmean_crystal_mask, "image", "kmean crystal mask")

    # ret, thresh = cv2.threshold(laplacian_uint8_filtered, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    # seg.disp_side_by_side(kmean_crystal_mask, thresh, "kmean crystal mask", "laplacian thresholding")


    seg.various_opening(kmean_crystal_mask, num_of_kernels=5, step_size=1, max_iteration=3)
    # seg.various_erosion(kmean_crystal_mask, num_of_kernels=4, step_size=2, max_iteration=3)
    # seg.various_dilation(kmean_crystal_mask, num_of_kernels=4, step_size=2, max_iteration=3)

    opening = cv2.morphologyEx(kmean_crystal_mask, cv2.MORPH_OPEN, kernel=np.ones((2,2), np.uint8), iterations= 3)
    seg.disp_side_by_side(kmean_crystal_mask, opening, "kmean crystal mask", "opening")
    seg.various_closing(opening, num_of_kernels=5, step_size=1, max_iteration=3)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel= np.ones((2,2), np.uint8), iterations= 3)
    seg.disp_side_by_side(opening, closing, "opening", "closing")

    seg.various_dilation(closing, num_of_kernels=4, step_size=2, max_iteration=3)
    sure_bg = cv2.dilate(closing, kernel=np.ones((17,17), np.uint8), iterations=1)
    seg.disp_side_by_side(kmean_crystal_mask, sure_bg, "kmean crystal mask", "sure_bg")

    seg.various_erosion(closing, num_of_kernels=4, step_size=2, max_iteration=3)
    sure_fg = cv2.erode(closing, kernel=np.ones((4,4), np.uint8), iterations=2)

    seg.disp_side_by_side(kmean_crystal_mask, sure_fg, "kmean crystal mask", "sure_fg")

    sure_fg = np.uint8(sure_fg)
    sure_bg = np.uint8(sure_bg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    seg.disp_side_by_side(image, unknown, "original image", "unknown region")

    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers +1
    markers[unknown==255] = 0
    seg.disp_side_by_side(image, markers, "original image", "watershed markers")

    laplacian_3D= seg.laplacian(image, output_dim=3)
    laplacian_3D_inv = 255- laplacian_3D
    io.imshow(laplacian_3D_inv)
    io.show()

    markers_origin_image = cv2.watershed(image, copy.copy(markers))
    image_copy = copy.copy(image)
    image_copy[markers_origin_image == -1] = [255, 0, 0]
    io.imshow(image_copy)
    io.show()

    markers_laplacian = cv2.watershed(laplacian_3D_inv, copy.copy(markers))
    image_copy = copy.copy(image)
    image_copy[markers_laplacian == -1] = [255, 0, 0]
    io.imshow(image_copy)
    io.show()


    kmean_image_3D = seg.kmeans_image(laplacian_3D, label)
    markers_kmean = cv2.watershed(kmean_image_3D, copy.copy(markers))
    image_copy = copy.copy(image)
    image_copy[markers_kmean == -1] = [255, 0, 0]
    io.imshow(image_copy)
    io.show()
    seg.disp_side_by_side(markers_laplacian, markers_kmean, "marker with laplacian image", "marker with kmean image")


    crystals_mask = np.zeros(image.shape)
    crystals_mask[markers_laplacian>1] = 255 #markers =1 means background
    crystals_mask = np.uint8(crystals_mask)

    image_copy = copy.copy(image)
    image_copy[crystals_mask!=255] = 0
    seg.disp_side_by_side(crystals_mask, image_copy, "crystal mask", "all crystals")

    ret, markers2= cv2.connectedComponents(kmean_crystal_mask)
    crystals_mask_kmean = np.zeros(image.shape)
    crystals_mask_kmean[markers2>0] = 255
    crystals_mask_kmean = np.uint8(crystals_mask_kmean)

    image_copy = copy.copy(image)
    image_copy[crystals_mask_kmean!= 255] = 0
    seg.disp_side_by_side(crystals_mask_kmean, image_copy, "crystal mask kmean", "all crystals")

    max_area_crystal_label = seg.label_of_max_watershed_area(markers_laplacian)
    max_area_crystal_mask = np.zeros(image.shape)
    max_area_crystal_mask[markers_laplacian==max_area_crystal_label] =255
    image_copy = copy.copy(image)
    image_copy[max_area_crystal_mask != 255] = 0
    seg.disp_side_by_side(image, image_copy, "original image", "biggest crystal")

    max_area_crystal_kmean = seg.extract_connected_component(kmean_crystal_mask, 8)
    image_copy = copy.copy(image)
    image_copy[max_area_crystal_kmean != 255] = 0
    seg.disp_side_by_side(image, image_copy, "original image", "biggest crystal (by kmean)")

