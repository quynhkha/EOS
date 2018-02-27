import builtins
# make dir
import os
import shutil

import PIL
import numpy as np
from PIL import Image

from EOSWebApp.imageProcessing import FindingHoles
from EOSWebApp.imageProcessing.utils import findImageDir

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
findDir = findImageDir()

class FindSegment():
    def __init__(self):
        self.processedFolderDir = ""


    def saveAndReturnImageURL(self, image, imageDir, mode=None):
        if mode == None:
            im = Image.fromarray(image, mode='L')
        else:
            im = Image.fromarray(image, mode= mode)
        fp = builtins.open(imageDir, "wb+")
        im.save(fp)

        processedImageURL = '/media/' + os.path.basename(imageDir)
        print ("processedImageURL", processedImageURL)
        return processedImageURL

    def save_an_image_copy(self, db_image, db_image_dir):
        #image_copy name
        image_copy_name = db_image.imageName + "_copy"
        #image_copy dir
        db_image_dir= findDir.imageDirfromDatabaseImg(db_image)
        image_copy_dir= os.path.join(BASE_DIR,
                                     '../../EOSWebApp/../../../media') + "/" + image_copy_name + '.' + db_image.imageType
        #make a copy of db_image
        shutil.copy2(db_image_dir, image_copy_dir)
        return image_copy_dir

    def imageMasking(self, processed_image_dir, mask_size):
        processed_image = np.asarray(PIL.Image.open(processed_image_dir))
        image_masked = FindingHoles.masking(processed_image, mask_size)
        return self.saveAndReturnImageURL(image_masked, processed_image_dir)

    def imageDilate(self, processed_image_dir, dilate_size):
        processed_image = np.asarray(PIL.Image.open(processed_image_dir))
        image_dilated = FindingHoles.dilating(processed_image, dilate_size)
        return self.saveAndReturnImageURL(image_dilated, processed_image_dir)

    def imagePengzhang(self, db_image_dir, processed_image_dir):
        db_image = np.asarray(PIL.Image.open(db_image_dir))
        processed_image = np.asarray(PIL.Image.open(processed_image_dir))
        image_pengzhang = FindingHoles.pengzhang(db_image, processed_image)
        return self.saveAndReturnImageURL(image_pengzhang, processed_image_dir)

    def imageWindowing(self, processed_image_dir, window_size):
        processed_image = np.asarray(PIL.Image.open(processed_image_dir))
        image_windowed = FindingHoles.windowing(processed_image, window_size)
        return self.saveAndReturnImageURL(image_windowed, processed_image_dir)

    def imageOstu(self, processed_image_dir, ostu_size):
        processed_image = np.asarray(PIL.Image.open(processed_image_dir))
        image_ostu = FindingHoles.ostu(processed_image, ostu_size)
        return self.saveAndReturnImageURL(image_ostu, processed_image_dir, mode="I")

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