import matplotlib
import matplotlib.pyplot as plt
import os
from skimage import io
import numpy as np
import copy
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

# data_dir = '/home/long/PycharmProjects/EOS/ImageProcessing/data/'
# filename = os.path.join(data_dir, '1947-1_plg6.png')
# image = io.imread(filename)
# print ("image", image)
# # seed = np.copy(image)
# # seed [1:-1, 1:-1] = image.max()
# # mask = image
# # filled = reconstruction(seed, mask, method = 'erosion')
# #
# # plt.imshow(image, cmap='gray')
# # plt.show()
# print ('original shape',image.shape)
# print ('original max, min ', image.max(), image.min())
# #image = img_as_ubyte(image)
# # with warnings.catch_warnings():
# #      warnings.simplefilter("ignore")
# #      img_as_ubyte(image)
#
# image_bw = rgb2gray(copy.copy(image))
# print ('gray shape',image_bw.shape)
# print ('gray max, min ', image.max(), image.min())
# print ("image_bw", image_bw)
#
# io.imshow(image)
# io.show()


# #image = rescale_intensity(image, out_range= (0, 255))
# print ('rescaled shape', image.shape)
# print ('rescaled max, min', image.max(), image.min())
# print ('type image ', type(image))


################################
# make dir
import os
import errno
class FindSegment():
    def __init__(self):
        self.processedFolderDir = ""


    # def makeDir(self, folderDir):
    #     folderDir = folderDir+"- processed"
    #     try:
    #         os.makedirs(folderDir)
    #         self.processedFolderDir = copy.copy(folderDir)
    #     except OSError as exception:
    #         if exception.errno != errno.EEXIST:
    #             raise

    ################################
    #using mask
    def saveAndReturnImageURL(self, image, folderDir, isFirstStep):

        if isFirstStep:
            image_processed_dir = folderDir+ "-processed" + ".png"
        else:
            image_processed_dir = folderDir + ".png"
        im = Image.fromarray(image)
        im.save(image_processed_dir)

        processedImageURL = '/media/' + os.path.basename(image_processed_dir)
        return processedImageURL

    def imageMasking(self, imageDir,folderDir,  mask_size):
        image = io.imread(imageDir)
        image_mask = copy.copy(image)
        mask = image >mask_size
        #print ("mask", mask)

        image_mask[mask] = 255
        return self.saveAndReturnImageURL(image_mask, folderDir, True)
        # io.imshow(image_mask)
        # io.show()
        #print ("image_mask", image_mask)

    def imageDilate(self, imageDir, folderDir, dilate_size):
        image = io.imread(imageDir)
        strel3 = morph.rectangle(3, 3)  # square shape with size of 3
        image_dilate = morph.dilation(copy.copy(image), strel3)
        io.imshow(image_dilate)
        io.show()
        return self.saveAndReturnImageURL(image_dilate, folderDir, False)


#print (image_bw)
#image_mask = rgb2gray(image_mask)


#
# #################################
# #dilate image
# strel3 = morph.rectangle(3,3) #square shape with size of 3
# dilate = morph.dilation(copy.copy(image_mask), strel3)
# print('dilate shape ', dilate.shape)
# print ("dilate", dilate)
#
# io.imshow(dilate)
# io.show()
# # plt.imshow(dilate, cmap="gray")
# # plt.show()
#
# #####################################
# # #pic4
# mask2 = (dilate==0)
# print ("mask 2", mask2)
# image_mask2= copy.copy(image_bw)
# image_mask2[mask2]=255
#
# print ('image_mask2 max, min', image_mask2.max(), image_mask2.min())
# print ("image_mask2", image_mask2)
#
# io.imshow(image_mask2)
# io.show()
#
#
# # plt.imshow(image_mask2, cmap ='gray')
# # plt.show()
#
# #second implementation of the function)
#
# # image_dilate = copy.copy(image_bw)
# # (img_height, img_width) = image_dilate.shape
# # print ('dilate max, min', dilate.max(), dilate.min())
# # print ('image dilate max, min ', image_dilate.max(), image_dilate.min())
# #
# # for i in range (img_height):
# #     for j in range (img_width):
# #
# #         if (dilate[i,j] ==0.0):
# #             image_dilate[i,j] = 255.0
# #
# # plt.imshow(image_dilate, cmap ="gray")
# # plt.show()
#
# ###########################################
# window_size = 20
# zero_pixel = []
# image_zouwei = copy.copy(image_mask2)
# (img_height, img_width) = image_bw.shape
# mask3 = (image_mask2 ==0)
#
# for i in range (img_height):
#     for j in range (img_width):
# #     if (image_bw[i,j] ==0):
# #             zero_pixel.append((i,j))
#
#         if mask3[i][j] == True:
#             zero_pixel.append((i,j))
# for (i,j) in zero_pixel:
#     if (i>window_size and i<=img_height- window_size) \
#         and (j>window_size and j<=img_width - window_size):
#         zhouwei = copy.copy(image_zouwei[(i-window_size):(i+window_size), (j-window_size):(j+window_size)])
#         mean_zhouwei = copy.copy(np.mean(copy.copy(zhouwei)))
#         image_zouwei[i,j] = np.mean(copy.copy(zhouwei))
#
# io.imshow(image_zouwei)
# io.show()
#
# ################################################################
# #ostu
# image_ostu_origin = copy.copy(image_zouwei)
# rgb2gray(image_ostu_origin)
# io.imshow(image_ostu_origin)
# io.show()
#
# strel8 = morph.rectangle(8,8) #square shape with size of 8
# dilate_ostu = morph.dilation(copy.copy(image_ostu_origin), strel8)
# print('dilate ostu shape ', dilate_ostu.shape)
# print ("dilate_ostu", dilate_ostu)
#
# io.imshow(dilate_ostu)
# io.show()
#
#
# #################################################################
# #texture
# image_texture = copy.copy(dilate_ostu)
#
#
# ##################################################################
# #liantongyu
# image_liantongyu = copy.copy(image_texture)
# mask4 = (image_texture>np.mean(image_texture))
# image_liantongyu[mask4]=1
#
#
# #########################################################