import matplotlib
import matplotlib.pyplot as plt
import os
from skimage import io
import numpy as np
import copy
import oct2py
from PIL import Image

from skimage import data
from skimage.exposure import rescale_intensity
from skimage.morphology import reconstruction
from skimage.color import rgb2gray
from skimage import img_as_ubyte
from skimage import img_as_uint
import warnings
from skimage.morphology import disk

import skimage.morphology as morph
from skimage.filters import rank

data_dir = '/home/long/PycharmProjects/EOS/ImageProcessing/data/'
filename = os.path.join(data_dir, '1947-1_plg6.png')
image = io.imread(filename)

oc = oct2py.Oct2Py()
oc.load

image2 = oc.imread(filename)
def convert_to_bw(np_image):
    PILimage= Image.fromarray(np_image)
    gray=PILimage.convert('L')
    bw = np.asarray(gray).copy()
    bw[bw < 128] = 0  # Black
    bw[bw >= 128] = 1  # White
    return bw

def bw_invert(np_bw):
    return 1-np_bw

def bwlabel(np_bw, size):
    np_img = oc.bwlabel(np_bw, size)
    return np_img

def show_np_img(np_img):
    plt.imshow(np_img, cmap ='gray')
    plt.show()


print ('original shape',image.shape)
print ('original max, min ', image.max(), image.min())
#image = img_as_ubyte(image)
# with warnings.catch_warnings():
#      warnings.simplefilter("ignore")
#      img_as_ubyte(image)

image_bw = rgb2gray(copy.copy(image))
print ('gray shape',image_bw.shape)
print ('gray max, min ', image.max(), image.min())
print ("image_bw", image_bw)

io.imshow(image)
io.show()

image_mask = copy.copy(image_bw)
mask = image_bw >5
print ("mask", mask)
image_mask[mask] = 255
print ("image_mask", image_mask)
#print (image_bw)
#image_mask = rgb2gray(image_mask)

io.imshow(image_mask)
io.show()

#################################
#dilate image
strel3 = morph.rectangle(3,3) #square shape with size of 3
dilate = morph.dilation(copy.copy(image_mask), strel3)
print('dilate shape ', dilate.shape)
print ("dilate", dilate)

io.imshow(dilate)
io.show()
# plt.imshow(dilate, cmap="gray")
# plt.show()

#####################################
# #pic4
mask2 = (dilate==0)
print ("mask 2", mask2)
image_mask2= copy.copy(image_bw)
image_mask2[mask2]=255

print ('image_mask2 max, min', image_mask2.max(), image_mask2.min())
print ("image_mask2", image_mask2)

io.imshow(image_mask2)
io.show()


# plt.imshow(image_mask2, cmap ='gray')
# plt.show()

#second implementation of the function)

# image_dilate = copy.copy(image_bw)
# (img_height, img_width) = image_dilate.shape
# print ('dilate max, min', dilate.max(), dilate.min())
# print ('image dilate max, min ', image_dilate.max(), image_dilate.min())
#
# for i in range (img_height):
#     for j in range (img_width):
#
#         if (dilate[i,j] ==0.0):
#             image_dilate[i,j] = 255.0
#
# plt.imshow(image_dilate, cmap ="gray")
# plt.show()

###########################################
window_size = 20
zero_pixel = []
image_zouwei = copy.copy(image_mask2)
(img_height, img_width) = image_bw.shape
mask3 = (image_mask2 ==0)

for i in range (img_height):
    for j in range (img_width):
#     if (image_bw[i,j] ==0):
#             zero_pixel.append((i,j))

        if mask3[i][j] == True:
            zero_pixel.append((i,j))
for (i,j) in zero_pixel:
    if (i>window_size and i<=img_height- window_size) \
        and (j>window_size and j<=img_width - window_size):
        zhouwei = copy.copy(image_zouwei[(i-window_size):(i+window_size), (j-window_size):(j+window_size)])
        mean_zhouwei = copy.copy(np.mean(copy.copy(zhouwei)))
        image_zouwei[i,j] = np.mean(copy.copy(zhouwei))

io.imshow(image_zouwei)
io.show()

################################################################
#ostu
image_ostu_origin = copy.copy(image_zouwei)
image_ostu_bw = convert_to_bw(image_ostu_origin)
show_np_img(image_ostu_bw)

strel8 = morph.rectangle(8,8) #square shape with size of 8
dilate_ostu = morph.dilation(copy.copy(image_ostu_bw), strel8)
print('dilate ostu shape ', dilate_ostu.shape)
print ("dilate_ostu", dilate_ostu)

show_np_img(dilate_ostu)


#################################################################
#texture
image_texture = copy.copy(dilate_ostu)


##################################################################
#liantongyu
image_liantongyu = copy.copy(image_texture)
print ('image_liantongyu', image_)
# mask4 = (image_texture>np.mean(image_texture))
# image_liantongyu[mask4]=1

image_liantongyu_bw_inv = bw_invert(image_liantongyu)
np_labeled = bwlabel(image_liantongyu,4)
show_np_img(np_labeled)

#########################################################
