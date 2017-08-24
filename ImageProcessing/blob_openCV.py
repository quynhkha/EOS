# Import relevant libraries
import os

import numpy as np
import cv2

data_dir = '/home/long/PycharmProjects/EOS/ImageProcessing/data/'
code_dir = '/home/long/PycharmProjects/EOS/ImageProcessing/'
filename = os.path.join(data_dir, '1947-1_plg6.png')

# Read in image and convert to grayscale
im1 = cv2.imread(filename)
im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)

# Adaptive Threshold
thresh = cv2.adaptiveThreshold(im1, 255,
                            adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                            thresholdType=cv2.THRESH_BINARY_INV,
                            blockSize=21,
                            C=2)

# Morphology to close gaps
se = cv2.getStructuringElement(cv2.MORPH_RECT, (15,15))
out = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, se)

# Find holes
mask = np.zeros_like(im1)
cv2.floodFill(out[1:-1,1:-1].copy(), mask, (0,0), 255)
mask = (1 - mask).astype('bool')

# Fill holes
out[mask] = 255

# Find contours
_, contours,_ = cv2.findContours(out.copy(),
                              cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_NONE)

# Filter out contours with less than certain area
area = 50000
filtered_contours = filter(lambda x: cv2.contourArea(x) > area,
                           contours)

# Draw final contours
final = np.zeros_like(im1)
try:
    cv2.drawContours(final, filtered_contours, -1, 255, -1)
except:
    print("value doesn't exist yet")
cv2.imshow('Shapes', final)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('train1_final.png', final)