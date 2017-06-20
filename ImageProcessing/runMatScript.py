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

image = io.imread(filename)

io.imshow(image)
io.show()
oc = oct2py.Oct2Py()
oc.load
oc.load

region_prop = os.path.join(code_dir, 'regionprop.m')
oc.addpath(region_prop)
index = oc.regionprop(image)
# print(stats)
# print(area)
print(index)

checkandshow = os.path.join(code_dir, 'checkandshow.m')
oc.addpath(checkandshow)
image2 = oc.checkandshow(image, copy.copy(index))
print (image2)