import copy
import cv2
import numpy as np
from skimage import io, img_as_ubyte
from matplotlib import pyplot as plt
from skimage import measure
from scipy import ndimage

class Segment:
    def __init__(self, segments=5):
        # define number of segments, with default 5
        self.segments = segments

    def kmeans(self, image):
        #Preprocessing step
        image = cv2.GaussianBlur(image, (3,3), 0)
        vectorized = image.reshape(-1,3)
        vectorized = np.float32(vectorized)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, label, center = cv2.kmeans(vectorized, self.segments, None,
                                        criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        res = center[label.flatten()]
        segmented_image = res.reshape((image.shape))
        return label.reshape((image.shape[0], image.shape[1])),segmented_image.astype(np.uint8)

    def extractComponent(self, image, label_image):
        image_segmented = np.zeros(image.shape)
        for i in range(5):
            image_segmented[label_image == i] = 255- i*60
        #image_segmented[label_image ==2 ] = 255

        return image_segmented
        # component = np.ones(image.shape, np.uint8)
        # component[label_image == label] = image[label_image == label]
        # return component
    def connectedComponent(self, binary_image, connectivity):
        #img_grey = cv2.cvtColor(binary_image, cv2.COLOR_BGR2GRAY)

        #ret, thresh = cv2.threshold(img_grey, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        unit8_img = img_as_ubyte(binary_image)
        ret, thresh = cv2.threshold(unit8_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # Perform operation
        output = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S)
        # Get the results
        num_labels = output[0]

        labels = output[1]
        # stat matrix
        stats = output[2]
        # centroid matrix
        centroids = output[3]

        fg_area=stats[1:,4]
        max_fg_area_index=np.argmax(fg_area)
        max_area_coordinate=stats[max_fg_area_index+1, 0:4]
        max_fg_area = stats[max_fg_area_index+1, 4]
        max_area_centroid = centroids[max_fg_area_index+1]

        max_area_img = np.zeros(unit8_img.shape)
        max_area_img[labels==(max_fg_area_index+1)] = 255

        return max_area_img, num_labels, stats, max_fg_area_index

    def sure_fg(self, image):
        kernel = np.ones((5,5), np.uint8)
        erosion = cv2.erode(image, kernel, iterations=1)
        seg.disp_img_with_title(erosion,"erosion-find_sure_fg")
        sure_fg, num_labels, stat, max_fg_index = seg.connectedComponent(erosion, 8)
        seg.disp_img_with_title(sure_fg, "sure_fg")
        return sure_fg

    def sure_bg(self, image):
        kernel = np.ones((1,1), np.uint8)
        erosion = cv2.erode(image, kernel, iterations=1)
        seg.disp_img_with_title(erosion,"erosion-find_sure_bg")

        dilation = cv2.dilate(image, kernel, iterations=1)
        seg.disp_img_with_title(dilation, "dilation-find_sure_bg")
        sure_bg, num_labels, stat, max_fg_index = seg.connectedComponent(erosion, 8)
        seg.disp_img_with_title(sure_bg, "sure_bg")

        return sure_bg

    def watershed_markers(self, sure_fg, unknown):
        # Marker labelling
        ret, markers = cv2.connectedComponents(sure_fg)
        # Add one to all labels so that sure background is not 0, but 1
        markers = markers + 1
        # Now, mark the region of unknown with zero
        markers[unknown == 255] = 0
        seg.disp_img_with_title(markers, "watershed marker")
        return markers

    def extractCrystal(self, image, label_image):
        image_segmented = np.zeros(image.shape, dtype=np.uint8)
        image_segmented[label_image == 2] = 255
        return image_segmented

    def extractCrystal_3D(self, image, label_image):
        image_segmented = np.zeros(image.shape, dtype=np.uint8)
        image_segmented[label_image == 2] = 255
        return image_segmented

    def region_prop(self, image):
        # label_img = measure.label(image)
        str_3D=np.array([[[0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]],

        [[0, 1, 0],
            [1, 1, 1],
        [0, 1, 0]],

        [[0, 0, 0],
            [0, 0, 0],
        [0, 0, 0]]], dtype='uint8')

        str_2D = np.array( [[1,1,1],
             [1,1,1],
             [1,1,1]])

        label_img, num_of_features = ndimage.measurements.label(image, str_2D)
        print("num of features ", num_of_features)
        regions = measure.regionprops(label_img)
        region_area = []
        for region in regions:
            print(region.coords)
            # [_, _, label] = region.coords[0]
            region_area.append(region.area)
            # if label == 2:
            #     region_area.append(region.area)

        max_value = max(region_area)
        max_index = region_area.index(max_value)
        print(max_value, max_index)
        max_region = regions[max_index]

        # (height, width) = im.shape
        # mask = np.zeros((height, width), )

        result = np.zeros(image.shape, np.uint8)
        print("max region 's coords", max_region.coords)
        for (row, col) in max_region.coords:
            result[row, col] = image[row, col]
        return result
        #
        # for region in regions:
        #     for prop in region:
        #         print(prop, region[prop])
    def thresholding(self, image, lower_val, upper_val):
        img_copy = copy.copy(image)

        lower_mask = img_copy<lower_val
        img_copy[lower_mask] = 0
        seg.disp_img_with_title(img_copy, "lower mask")

        upper_mask =img_copy>upper_val
        img_copy[upper_mask] =0
        seg.disp_img_with_title(img_copy, "upper mask")

        unit8_img = img_as_ubyte(img_copy[:, :, 0])
        ret, thresh = cv2.threshold(unit8_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        seg.disp_img_with_title(thresh, 'theshold + ostu')

        kernel = np.ones((3,3), np.uint8)

        closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
                                   kernel=np.ones((2,2), np.uint8))
        seg.disp_img_with_title(closing, 'closing')
        dilation = cv2.dilate(thresh, kernel=np.ones((2,2), np.uint8), iterations=1)
        seg.disp_img_with_title(dilation, "dilation")

        erosion = cv2.erode(dilation, kernel=np.ones((2,2), np.uint8), iterations=1)
        seg.disp_img_with_title(erosion, "erosion")
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

if __name__ == "__main__":
    import argparse
    import sys
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="Path to the image")
    ap.add_argument("-n", "--segments", required=False,
                    type=int, help="# of clusters")
    args = vars(ap.parse_args())

    image = cv2.imread(args["image"])


    if len(sys.argv) == 3:
        seg = Segment()
        label, result = seg.kmeans(image)
    else:
        seg = Segment(args["segments"])
        label, result = seg.kmeans(image)

    segmented_img = result
    binary_crystal_3D = seg.extractComponent(result, label)
    # io.imshow(binary_crystal_3D, cmap='gray')
    # io.show()
    seg.disp_side_by_side(image, binary_crystal_3D, "original", "kmeans")

    thresh = seg.thresholding(image, 70, 100)
    distance = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    seg.disp_img_with_title(distance, 'distance transform')

    binary_crystal = seg.extractCrystal(result[:, :, 0], label)
    io.imshow(binary_crystal)
    io.show()

    kernel = np.ones((3, 3), np.uint8)

    # closing = cv2.morphologyEx(binary_crystal, cv2.MORPH_CLOSE, kernel)
    # io.imshow(closing)
    # io.show()

    opening = cv2.morphologyEx(binary_crystal, cv2.MORPH_OPEN, kernel)
    seg.disp_img_with_title(opening, "opening")
    # erosion = cv2.erode(opening, kernel, iterations=1)
    # io.imshow(erosion)
    # io.show()
    # dilation = cv2.dilate(erosion, kernel, iterations=1)
    # io.imshow(dilation)
    # io.show()

   # crystal, num_labels, stat, max_fg_index = seg.connectedComponent(erosion, 8)

    # sure_fg = seg.sure_fg(opening)
    sure_fg= seg.sure_fg(thresh)
    sure_fg = np.uint8(sure_fg)
    # sure_bg = seg.sure_bg(opening)
    sure_bg = seg.sure_bg(thresh)
    sure_bg = np.uint8(sure_bg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    unknown = np.uint8(unknown)
    seg.disp_img_with_title(unknown,"unknown_region")
    markers = seg.watershed_markers(np.uint8(sure_fg), unknown)

    # markers = np.uint32(markers)
    binary_crystal_3D = seg.extractCrystal_3D(result, label)
    markers = cv2.watershed(binary_crystal_3D, markers)
    print(markers)

    image[markers == -1] = [255, 0, 0]
    io.imshow(image)
    io.show()

    # result_img = seg.extractComponent(result, label, 2) #2D image
    # max_area_img = seg.region_prop(result_img[:, :, 0])
    # plt.imshow(max_area_img, cmap=plt.get_cmap('gray'))
    # plt.show()
    #
    # titles = ["extracted", "max area"]
    # images = [result_img, max_area_img]
    # for i in range(2):
    #     plt.subplot(1, 2, i+1), plt.imshow(images[i], cmap = 'gray')
    #     plt.title(titles[i])
    #     plt.xticks([ ]), plt.yticks([])
    # plt.show()
    # titles = ["segmented", "extracted"]
    # images = [segmented_img, result_img]
    #
    # for i in range(2):
    #     plt.subplot(2, 1, i + 1), plt.imshow(images[i], 'gray')
    #     plt.title(titles[i])
    #     plt.xticks([]), plt.yticks([])
    # plt.show()


#python3 kmean_clustering.py -i /home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.png -n 3
cv2.distanceTransform()