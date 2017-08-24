import os
import math
import copy
from skimage import io, filters, segmentation, color
import cv2
from skimage.future import graph
from skimage import measure, morphology

from PIL import Image, ImageFilter
import sklearn.cluster
import numpy as np

data_dir = '/home/long/PycharmProjects/EOS/ImageProcessing/data/'
code_dir = '/home/long/PycharmProjects/EOS/ImageProcessing/'
filename = os.path.join(data_dir, '1947-1_plg6.png')
#
# image = Image.open(filename)
# image = image.filter(ImageFilter.FIND_EDGES)
# image.show()

im = io.imread(filename)
io.imshow(im)
io.show()
print ("image shape", im.shape)
# edges = filters.sobel(im)
# io.imshow(edges)

# quickshift_img = segmentation.quickshift(im)
# io.imshow(quickshift_img)
# io.show()

import matplotlib
import matplotlib.pyplot as plt

from skimage import data
from skimage.filters import try_all_threshold

#img = data.page()

#
# fig, ax = try_all_threshold(im, figsize=(10, 8), verbose=False)
# plt.show()


img_copy = copy.copy(im)
# mask_min = img_copy<55
# img_copy[mask_min] = 0
# io.imshow(img_copy)
# io.show()
# mask_max =img_copy>95
# img_copy[mask_max] =0
# io.imshow(img_copy)
# io.show()

# img_2 = copy.copy(img_copy)
# selem = morphology.disk(1)
# percentile_result = filters.rank.mean_percentile(img_2, selem=selem, p0=.1, p1=.9)
# io.imshow(percentile_result)
# io.show()
#
#
# block_size =199
# adaptive_thresh = filters.threshold_local(percentile_result, block_size)
# binary_adaptive = copy.copy(img_copy)>adaptive_thresh
# io.imshow(binary_adaptive)
# io.show()



ret, thresh = cv2.threshold(img_copy,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

io.imshow(thresh)
io.show()

import scipy
from scipy import ndimage
import matplotlib.pyplot as plt

blur_radius = 3.0


# img = scipy.misc.imread(img_name) # gray-scale image
# print(img.shape)

# smooth the image (to remove small objects)
imgf = ndimage.gaussian_filter(thresh, blur_radius)
threshold = 30

# find connected components
labeled, nr_objects = ndimage.label(imgf > threshold)
print ("Number of objects is %d " % nr_objects)


plt.imsave('/tmp/out.png', labeled)
plt.imshow(labeled, "gray")

plt.show()

img_2 = copy.copy(img_copy)
selem = morphology.disk(1)
percentile_result = filters.rank.mean_percentile(img_2, selem=selem, p0=.1, p1=.9)
io.imshow(percentile_result)
io.show()



block_size =199
adaptive_thresh = filters.threshold_local(percentile_result, block_size)
binary_adaptive = copy.copy(img_copy)>adaptive_thresh
io.imshow(binary_adaptive)
io.show()

strel = morphology.rectangle(2,2)
dilate_image = morphology.dilation(binary_adaptive, strel)
io.imshow(dilate_image)
io.show()

label_img = measure.label(dilate_image)
regions = measure.regionprops(label_img)
region_area = []
for region in regions:
    region_area.append(region.area)

max_value = max(region_area)
max_index = region_area.index(max_value)
print(max_value, max_index)
max_region = regions[max_index]

# (height, width) = im.shape
# mask = np.zeros((height, width), )

result = np.zeros(im.shape, np.uint8)
for (row, col) in max_region.coords:
    result[row, col] = im[row, col]
io.imshow(result)
io.show()


for region in regions:
    for prop in region:
        print(prop, region[prop])



# edges = filters.sobel(binary_adaptive)
# io.imshow(edges)
# io.show()
# from skimage import data, io, segmentation, color
# from skimage.future import graph
# from matplotlib import pyplot as plt
#
#
# img = data.coffee()
#
# labels1 = segmentation.slic(img, compactness=30, n_segments=400)
# out1 = color.label2rgb(labels1, img, kind='avg')
#
# g = graph.rag_mean_color(img, labels1)
# labels2 = graph.cut_threshold(labels1, g, 29)
# out2 = color.label2rgb(labels2, img, kind='avg')
#
# fig, ax = plt.subplots(nrows=2, sharex=True, sharey=True,
#                        figsize=(6, 8))
#
# ax[0].imshow(out1)
# ax[1].imshow(out2)
#
# for a in ax:
#     a.axis('off')
#
# plt.tight_layout()
# mark_boundary_img = segmentation.mark_boundaries(im, mask)
# io.imshow(mark_boundary_img)
# io.show()

# slic_img = segmentation.slic(im, 100)
# io.imshow(slic_img)
# io.show()

# samples = np.column_stack(im.flatten())
# clf = sklearn.cluster.KMeans(n_clusters=5)
# labels = clf.fit_predict(im).reshape(im.shape)
# print(labels)
#
# import matplotlib.pyplot as plt
#
# plt.imshow(labels)
# plt.show()