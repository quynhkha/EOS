import os

import numpy as np
import cv2
from matplotlib import pyplot as plt
from skimage import io


data_dir = '/home/long/PycharmProjects/EOS/ImageProcessing/data/'
code_dir = '/home/long/PycharmProjects/EOS/ImageProcessing/'
filename = os.path.join(data_dir, '1947-1_plg6.png')
#
# image = Image.open(filename)
# image = image.filter(ImageFilter.FIND_EDGES)
# image.show()
def invert_img(img):
    return (255-img)

img = cv2.imread(filename)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ret,thresh1 = cv2.threshold(gray,90,255,cv2.THRESH_BINARY)
# ret,thresh2 = cv2.threshold(gray,90,255,cv2.THRESH_BINARY_INV)
# ret,thresh3 = cv2.threshold(gray,90,255,cv2.THRESH_TRUNC)
# ret,thresh4 = cv2.threshold(gray,90,255,cv2.THRESH_TOZERO)
# ret,thresh5 = cv2.threshold(gray,90,255,cv2.THRESH_TOZERO_INV)
# titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
# images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
# for i in range(6):
#     plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()

ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

io.imshow(thresh)
io.show()
thresh = invert_img(thresh)

# noise removal
kernel = np.ones((3,3), np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 4)

# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)


# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)


# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)


# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers+1

# Now, mark the region of unknown with zero
markers[unknown==255] = 0
'''
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgray = cv2.GaussianBlur(imgray, (5, 5), 0)
img = cv2.Canny(imgray,200,500)
'''
markers = cv2.watershed(img,markers)
img[markers == -1] = [255,0,0]

titles = ['background','foreground','threshold','result']
images = [sure_bg, sure_fg, thresh, img]

for i in range(4):
    plt.subplot(2, 2, i + 1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()


