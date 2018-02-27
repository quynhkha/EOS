import matplotlib
import matplotlib.pyplot as plt
import os
from skimage import io
import numpy as np
# np.set_printoptions(threshold=np.inf)
import copy
import oct2py
from PIL import Image

from skimage.color import rgb2gray
from skimage import img_as_ubyte
from skimage import img_as_uint
import warnings
from skimage.morphology import disk

import skimage.morphology as morph
from skimage.filters import rank


oc = oct2py.Oct2Py()
oc.load

def show_np_img(np_img):
    plt.imshow(np_img, cmap ='gray')
    print(np_img)
    plt.show()

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

    # io.imshow(np_bw)
    # io.show()
    return np_bw

def dilating(np_image, dilate_num):
    np_bw = copy.copy(np_image)
    strel = morph.rectangle(dilate_num, dilate_num)  # square shape with size of dilate_num
    dilate = morph.dilation(np_bw, strel)
    #np.savetxt("dilate.csv", dilate, delimiter=",")
    # print('dilate shape ', dilate.shape)
    # print("dilate", dilate)
    #
    # io.imshow(dilate)
    # io.show()
    return dilate

def pengzhang (original_bw, dilate):
    image_copy = copy.copy(original_bw)
    dilate_copy = copy.copy(dilate)
    mask = (dilate_copy ==0)
    image_copy[mask] = 255
    #np.savetxt("pengzhang.csv", image_copy, delimiter=",")
    # print('image_pengzhang max, min', image_copy.max(), image_copy.min())
    # print("image_pengszhang", image_copy)
    #
    # io.imshow(image_copy)
    # io.show()
    return image_copy

def windowing(np_image, window_size):
    zero_pixel = []
    np_bw = copy.copy(np_image)
    (img_height, img_width) = np_bw.shape
    mask = (np_image == 0)

    for i in range(img_height):
        for j in range(img_width):
            if mask[i][j] == True:
                zero_pixel.append((i,j))
    for (i, j) in zero_pixel:
        if (i > window_size and i <= img_height - window_size) \
                and (j > window_size and j <= img_width - window_size):
            zhouwei = copy.copy(np_bw[(i-window_size):(i+window_size), (j-window_size):(j+window_size)])
            mean_zhouwei = copy.copy(np.mean(copy.copy(zhouwei)))
            np_bw[i, j] = np.mean(copy.copy(zhouwei))
    #np.savetxt("windowing.csv", np_bw, delimiter=",")
    # io.imshow(np_bw)
    # io.show()
    return np_bw

def ostu(np_image, dilate_number):
    image = copy.copy(np_image)
    image_bw = convert_to_bw(image)
    # print ("image_bw")
    # io.imshow(image_bw)
    # io.show()

    dilate_ostu = dilating(image_bw, dilate_number)
    # print("dilate_ostu", dilate_ostu)
    #np.savetxt("ostu.csv", dilate_ostu, delimiter=",")

    show_np_img(dilate_ostu)
    return dilate_ostu

def convert_to_bw(np_image):
    np_image_copy = copy.copy(np_image)
    PILimage= Image.fromarray(np_image_copy)
    gray=PILimage.convert('L')
    bw = np.asarray(gray).copy()
    bw[bw < 128] = 0  # Black
    bw[bw >= 128] = 1  # White
    return bw
def convert_to_bw_for_disp(np_image):
    np_image_copy = copy.copy(np_image)
    PILimage = Image.fromarray(np_image_copy)
    gray = PILimage.convert('L')
    bw = np.asarray(gray).copy()
    bw[bw < 128] = 0  # Black
    bw[bw >= 128] = 255  # White
    return bw

def bw_invert(np_bw):
    return 1-np_bw

def bwlabel(np_image, size):
    np_bw = copy.copy(np_image)
    np_img = oc.bwlabel(np_bw, size)
    return np_img

def liantongyu (np_image):
    bw_image = copy.copy(np_image)
    bw_image_inv = bw_invert(bw_image)
    labeled_image = bwlabel(bw_image_inv,4)
    show_np_img(convert_to_bw_for_disp(labeled_image))
   #labeled_image_bw=convert_to_bw(labeled_image)
    return labeled_image


def region_prop(np_img):
    np_image = copy.copy(np_img)
    region_prop = os.path.join(code_dir, 'regionprop2.m')
    oc.addpath(region_prop)
    area = oc.regionprop(np_image)
    return area

def region_prop_index(np_img):
    np_image = copy.copy(np_img)
    region_prop = os.path.join(code_dir, 'regionprop.m')
    oc.addpath(region_prop)
    index = oc.regionprop(np_image)
    return index

def findMaxElementIndex(area):
    area_arr = copy.copy(area)
    index_of_max_element = np.argmax(area_arr)
    print(index_of_max_element)
    return index_of_max_element


# convert all pixel not equal index -> 0 and only pixel equal to index ->1
def changeIndexEquivalentPixel(np_image, index):
    image_copy = copy.copy(np_image)
    mask1 = (image_copy == index)
    image[mask1] = 0
    mask2 = (image_copy != index)
    image[mask2] = 1
    return image_copy


def findAreaAndIndex(bw_img):
    bw_image = copy.copy(bw_img)
    bw_image_inv = bw_invert(bw_image)
    labeled_image = bwlabel(bw_image_inv, 4)
    show_np_img(convert_to_bw_for_disp(labeled_image))
    area = region_prop(labeled_image)
    [area_value, indexLL] = oc.sort(area, 'descend')
    return labeled_image, area, indexLL

def checkAndShow(origin_img,lian_img, labeled_img, areaLL, indexLL):
    checkandshowsimple= os.path.join(code_dir, 'checkandshowsimple.m')
    oc.addpath(checkandshowsimple)
    image_checkandshow = oc.checkandshowsimple(copy.copy(origin_img), copy.copy(lian_img), copy.copy(labeled_img), areaLL, indexLL)

    show_np_img(image_checkandshow)
    return image_checkandshow



# image_mask= masking(image, 5)
# image_dilate = dilating(image_mask, 3)
# image_pengzhang = pengzhang(image, image_dilate)
# image_windowing = windowing(image_pengzhang,20)
# image_ostu = ostu(image_windowing, 8)
# image_liantongyu = liantongyu(image_ostu)
#
# # area = region_prop(image_liantongyu)
# # index = findMaxElementIndex(area)
# # index_image = changeIndexEquivalentPixel(image_liantongyu,index)#LL
# #
# # final_labeled_img, final_area, final_indexLL = findAreaAndIndex(index_image)
# #
# # img_check_and_show = checkAndShow(image, image_liantongyu, final_labeled_img, final_area, final_indexLL)
#
#
#
# #stats = oc.regionprops(copy.copy(image_liantongyu), 'Area')
# # print ('stat')
# # print (stats)
# # area = oc.cat(1, stats.Area)
# # max_area = oc.max(area)
# # index = oc.find(area == max_area)
# #
# # print (index)
#
#
#
# index = region_prop_index(image_liantongyu)
# print('index', index)
#
# checkandshow = os.path.join(code_dir, 'checkandshow.m')
# oc.addpath(checkandshow)
# image_checkandshow = oc.checkandshow(copy.copy(image), copy.copy(image_liantongyu), copy.copy(int(index)))
# print (image_checkandshow)
# # image_checkandshow_bw = convert_to_bw(copy.copy(image_checkandshow))
# # io.imshow(convert_to_bw_for_disp(image_checkandshow))
# show_np_img(image_checkandshow)
#



