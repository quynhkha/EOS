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

data_dir = '/home/long/PycharmProjects/EOS/ImageProcessing/data/'
code_dir = '/home/long/PycharmProjects/EOS/ImageProcessing/'
filename = os.path.join(data_dir, '1947-1_plg6.png')
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


image = np.asarray(Image.open(filename))
im_masked = masking (image, 5)
image_masked = Image.fromarray(im_masked)
image_masked.save(fp = "masked_image.png")

image2 = Image.open("masked_image.png")
io.imshow(np.asarray(image2))
io.show()