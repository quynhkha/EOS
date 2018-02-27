import numpy as np
import cv2 as cv
from skimage import io
from matplotlib import pyplot as plt

roi = cv.imread('/home/long/PycharmProjects/EOS/ImageProcessing/data/template4.png')
# roi = cv.imread('/home/long/Desktop/grass.jpg')
hsv = cv.cvtColor(roi,cv.COLOR_BGR2HSV)
target = cv.imread('/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg1.tif')
# target = cv.imread('/home/long/Desktop/messi.jpg')
hsvt = cv.cvtColor(target,cv.COLOR_BGR2HSV)
# calculating object histogram
roihist = cv.calcHist([hsv],[0, 1], None, [256, 256], [0, 256, 0, 256] )
# normalize histogram and apply backprojection
cv.normalize(roihist,roihist,0,255,cv.NORM_MINMAX)
dst = cv.calcBackProject([hsvt],[0,1],roihist,[0,256,0,256],1)
# Now convolute with circular disc
disc = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
cv.filter2D(dst,-1,disc,dst)
# threshold and binary AND
ret,thresh = cv.threshold(dst,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
# ret,thresh = cv.threshold(dst,0,255, 0)
thresh = cv.merge((thresh,thresh,thresh))
res = cv.bitwise_and(target,thresh)
res = np.vstack((target,thresh,res))

plt.subplot(121),plt.imshow(res,cmap = 'gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.show()