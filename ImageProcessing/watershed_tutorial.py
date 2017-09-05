import numpy as np
import cv2
from matplotlib import pyplot as plt

def disp_side_by_side(image1, image2, label1, label2):
    titles = [label1, label2]
    images = [image1, image2]
    for i in range(2):
        plt.subplot(1, 2, i + 1), plt.imshow(images[i], cmap='gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()

def disp_img_with_title(image, title):
    plt.subplot(1, 1, 1), plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.xticks([]), plt.yticks([])
    plt.show()

img = cv2.imread('/home/long/coins.jpg')
disp_img_with_title(img, 'original image')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
disp_img_with_title(gray, 'gray image')
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
disp_img_with_title(thresh, 'thresholded image')

# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
disp_img_with_title(opening, 'opening')
# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)
disp_img_with_title(sure_bg, 'sure_bg')
# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
disp_img_with_title(dist_transform, 'distance transform')
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
disp_img_with_title(sure_fg, 'sure_fg')
# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)
disp_img_with_title(unknown, 'unknown region')

# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)
disp_img_with_title(markers, 'markers')
# Add one to all labels so that sure background is not 0, but 1
markers = markers+1
disp_img_with_title(markers, 'markers modified')
# Now, mark the region of unknown with zero
markers[unknown==255] = 0
disp_img_with_title(markers, 'unknown region to zero')

markers = cv2.watershed(img,markers)
disp_img_with_title(markers, 'watershed')
img[markers == -1] = [255,0,0]
disp_img_with_title(img, 'watersheded image')