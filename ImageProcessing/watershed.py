import numpy as np
from skimage import io
import cv2
from matplotlib import pyplot as plt


img_name = '/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.png'
# img = cv2.imread(img_name)
#
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
#
# io.imshow(thresh)
# io.show()
#
# # noise removal
# kernel = np.ones((3,3),np.uint8)
# opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
# io.imshow(opening)
# io.show()
#
# # sure background area
# sure_bg = cv2.dilate(opening,kernel,iterations=3)
# io.imshow(sure_bg)
# io.show()
#
# # Finding sure foreground area
# dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
# ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
# io.imshow(sure_fg)
# io.show()
#
# # Finding unknown region
# sure_fg = np.uint8(sure_fg)
# unknown = cv2.subtract(sure_bg,sure_fg)
# io.imshow(unknown)
# io.show()


import scipy
from scipy import ndimage
import matplotlib.pyplot as plt

blur_radius = 1.0
threshold = 50


img = scipy.misc.imread(img_name) # gray-scale image
print(img.shape)

# smooth the image (to remove small objects)
imgf = ndimage.gaussian_filter(img, blur_radius)
threshold = 100

# find connected components
labeled, nr_objects = ndimage.label(imgf > threshold)
print ("Number of objects is %d " % nr_objects)

plt.imsave('/tmp/out.png', labeled)
plt.imshow(labeled, "gray")

plt.show()