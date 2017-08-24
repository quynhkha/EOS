import os
from math import sqrt

import copy
from skimage import data, io, measure, img_as_ubyte, img_as_float
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.color import rgb2gray

import matplotlib.pyplot as plt
import skimage.morphology as morph

import numpy as np

# image = data.hubble_deep_field()[0:500, 0:500]
data_dir = '/home/long/PycharmProjects/EOS/ImageProcessing/data/'
code_dir = '/home/long/PycharmProjects/EOS/ImageProcessing/'
filename = os.path.join(data_dir, '1947-1_plg6.small.png')
image = io.imread(filename)

io.imshow(image)
io.show()
image_gray = rgb2gray(image)
#back to 0-255 with 1 channel
img_src = img_as_ubyte(image_gray)


def masking(np_image, mask_num):
    np_bw = copy.copy(np_image)
    mask = np_bw > mask_num
    print("mask", mask)
   # np.savetxt("mask.csv", mask, delimiter=",")

    np_bw[mask] = 255
    print("image_mask", np_bw)
    #np.savetxt("image_mask.csv", np_bw, delimiter=",")
    # print (image_bw)
    # image_mask = rgb2gray(image_mask)

    io.imshow(np_bw)
    io.show()
    return np_bw

def dilating(np_image, dilate_num):
    np_bw = copy.copy(np_image)
    strel = morph.rectangle(dilate_num, dilate_num)  # square shape with size of dilate_num
    dilate = morph.dilation(np_bw, strel)
    #np.savetxt("dilate.csv", dilate, delimiter=",")
    print('dilate shape ', dilate.shape)
    print("dilate", dilate)

    io.imshow(dilate)
    io.show()
    return dilate

def pengzhang (original_bw, dilate):
    image_copy = copy.copy(original_bw)
    dilate_copy = copy.copy(dilate)
    mask = (dilate_copy ==0)
    image_copy[mask] = 255
    #np.savetxt("pengzhang.csv", image_copy, delimiter=",")
    print('image_pengzhang max, min', image_copy.max(), image_copy.min())
    print("image_pengszhang", image_copy)

    io.imshow(image_copy)
    io.show()
    return image_copy

image_mask= masking(img_src, 5)
image_dilate = dilating(image_mask, 3)
image_pengzhang = pengzhang(img_src, image_dilate)





blobs_log = blob_log(image_pengzhang, max_sigma=30, num_sigma=10, threshold=.1)

# Compute radii in the 3rd column.
blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)

blobs_dog = blob_dog(image_gray, max_sigma=30, threshold=.1)
blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)

blobs_doh = blob_doh(image_gray, max_sigma=30, threshold=.01)

blobs_list = [blobs_log, blobs_dog, blobs_doh]
colors = ['yellow', 'lime', 'red']
titles = ['Laplacian of Gaussian', 'Difference of Gaussian',
          'Determinant of Hessian']
sequence = zip(blobs_list, colors, titles)

fig, axes = plt.subplots(1, 3, figsize=(9, 3), sharex=True, sharey=True,
                         subplot_kw={'adjustable': 'box-forced'})
ax = axes.ravel()

for idx, (blobs, color, title) in enumerate(sequence):
    ax[idx].set_title(title)
    ax[idx].imshow(image, interpolation='nearest')
    for blob in blobs:
        y, x, r = blob
        c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
        ax[idx].add_patch(c)
    ax[idx].set_axis_off()

plt.tight_layout()
plt.show()


# blob_labels = measure.label(blobs_log, background = 0)
# plt.imshow(blob_labels)
# plt.show()

# from sklearn.neighbors import NearestNeighbors
# points = []
# x_arr = []
# y_arr = []
# for i in range(len(blobs_log)):
#     y,x,_ = blobs_log[i]
#
#     points.append([x,y])
#     x_arr.append(x)
#     y_arr.append(y)
# print (points)
# clf = NearestNeighbors(2).fit(points)
# G = clf.kneighbors_graph()
#
# import networkx as nx
# T = nx.from_scipy_sparse_matrix(G)
# mindist = np.inf
# minidx = 0
# paths = [list(nx.dfs_preorder_nodes(T, i)) for i in range(len(points))]
# for i in range(len(points)):
#     p = paths[i]           # order of nodes
#     ordered = points[p]    # ordered nodes
#     # find cost of that order by the sum of euclidean distances between points (i) and (i+1)
#     cost = (((ordered[:-1] - ordered[1:])**2).sum(1)).sum()
#     if cost < mindist:
#         mindist = cost
#         minidx = i
# #
# opt_order = paths[minidx]
# # order = list(nx.dfs_preorder_nodes(T, 0))
# #
# # xx = x_arr[order]
# # yy = y_arr[order]
#
# xx = x_arr[opt_order]
# yy = y_arr[opt_order]
#
# plt.plot(xx, yy)
# plt.show()
#
# plt.plot(xx, yy)
# plt.show()

import cv2
# import numpy as np
# from matplotlib import pyplot as plt
# img = cv2.imread(filename,0)
# edges = cv2.Canny(img,100,200)
# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# plt.show()


im = cv2.imread(filename)
im_cv = image_pengzhang
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
# image = cv2.GaussianBlur(imgray, (7, 7), 0)
ret,thresh = cv2.threshold(imgray,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
max_area = 0
max_contour = contours[0]
choosen_contours = []
for contour in contours:
    area = cv2.contourArea(contour)
    if max_area< area:
        max_area = area
        max_contour = contour
    if area>100:
        choosen_contours.append(contour)
print (max_area)
print (max_contour)
print(choosen_contours)

cv2.drawContours(imgray, max_contour, -1, (0,255,0), 3)
cv2.drawContours(imgray, choosen_contours, -1, (255,0,0), 3)
plt.imshow(imgray)
plt.show()
