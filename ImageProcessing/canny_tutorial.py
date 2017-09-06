import cv2
import numpy as np
from matplotlib import pyplot as plt
import copy
from skimage import io, img_as_ubyte

def thresholding(image, lower_val, upper_val):
    '''
    Do thresholding to extract pixels within range.
    Do image enhancement with closing, dilation and erosion

    TODO: add closing, dilation and erosion kernel size and iterations num

    :param image: grayscale 3-channel image
    :param lower_val: lower threshold value
    :param upper_val: upper threshold value
    :return: binary image (single channel)
    '''
    img_copy = copy.copy(image)[:, :, 0]
    #img_copy = copy.copy(image)
    lower_mask = img_copy < lower_val
    img_copy[lower_mask] = 0

    upper_mask = img_copy > upper_val
    img_copy[upper_mask] = 0

    # change to single channel
    unit8_img = img_as_ubyte(img_copy)

    ret, thresh = cv2.threshold(unit8_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # remove the inner holes
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE,
                               kernel=np.ones((2, 2), np.uint8))

    dilation = cv2.dilate(thresh, kernel=np.ones((2, 2), np.uint8), iterations=1)


    erosion = cv2.erode(dilation, kernel=np.ones((2, 2), np.uint8), iterations=1)

    return erosion

def disp_side_by_side(image1, image2, label1, label2):
    titles = [label1, label2]
    images = [image1, image2]
    for i in range(2):
        plt.subplot(1, 2, i+1), plt.imshow(images[i], cmap = 'gray')
        plt.title(titles[i])
        plt.xticks([ ]), plt.yticks([])
    plt.show()
def connectedComponent(binary_image, connectivity):
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

    return np.uint8(max_area_img)

# img = cv2.imread('/home/long/opencv/samples/data/lena.jpg',0)
img = cv2.imread('/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.small.png')
img_1D = img[:, :, 0]
laplacian = cv2.Laplacian(img_1D,cv2.CV_64F)
laplacian_abs = np.absolute(laplacian)
laplacian_8U = np.uint8(laplacian_abs)
plt.imshow(laplacian_8U)
plt.show()
sobelx = cv2.Sobel(img_1D,cv2.CV_64F,1,0,ksize=5)
sobelx_8U = np.uint8(np.absolute(sobelx))
plt.imshow(sobelx_8U)
plt.show()
sobely = cv2.Sobel(img_1D,cv2.CV_64F,0,1,ksize=5)
sobely_8U = np.uint8(np.absolute(sobely))
gradmag = np.uint8(np.sqrt(sobelx_8U*sobelx_8U + sobely_8U*sobely_8U))
plt.subplot(2,2,1),plt.imshow(gradmag,cmap = 'gray')
plt.title('Gradient'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(laplacian_8U,cmap = 'gray')
plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(sobelx_8U,cmap = 'gray')
plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(sobely_8U,cmap = 'gray')
plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])
plt.show()

laplacian_1D = np.uint8(laplacian_8U)
ret, laplacian_thresh = cv2.threshold(laplacian_1D, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
plt.imshow(laplacian_thresh, cmap= 'gray')
plt.show()
#img = cv2.imread('/home/long/apple.jpg')
#img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

kernel = np.ones((3, 3), np.uint8)
#img = cv2.GaussianBlur(img, (5,5), 0)
thresh = thresholding(img,70,110)
disp_side_by_side(laplacian_thresh, thresh,"laplacian_thresh", "thresh")
edges = cv2.Canny(laplacian_1D,50,200)
connected = connectedComponent(laplacian_1D, 8)
disp_side_by_side(laplacian_thresh, connected, "laplacian thresh", "connected")
# contours = np.zeros(img.shape)
im2, contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE )
cv2.drawContours(img, contours, -1, (0,0,255), thickness=cv2.FILLED)
plt.subplot(121),plt.imshow(edges,cmap = 'gray')
plt.title('Canny'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img)
plt.title('Filled'), plt.xticks([]), plt.yticks([])

plt.show()