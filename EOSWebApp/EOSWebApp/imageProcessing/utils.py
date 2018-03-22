import os

import cv2
import numpy as np

from EOSWebApp.imageProcessing.models import TempImage, UploadedImage, TempMask
from EOSWebApp.utils import timing, thumbnail_plus_img_json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_UNDO_STEP = 10


# def absolute_uploaded_file_dir(url):
#      return str(BASE_DIR)+url



# from django.contrib.auth.models import User
# users = User.objects.all()
# print(users.values_list('password', flat=True))

# class TempData:
#     def __init__(self):
#         self.s_img_ori = StateImage('original image', np.zeros((400, 400), np.uint8))
#         self.s_img_cur = StateImage('current image', np.zeros((400, 400), np.uint8))
#         self.s_mask_cur = StateImage('current mask', np.zeros((400, 400), np.uint8))
#         self.s_img_last_arr = []
#         self.s_thumb_hist_arr = []
#         self.s_max_undo_step = 10
#         self.s_undo_depth = 1
#         self.s_last_cal_func = ""
#         self.s_labels = 0
#         self.s_just_recovered = False
#         self.user_id = ''
#         self.image_id = ''
#
#     def update_s_img_cur(self, func_name, img_data, gray_levels=''):
#         self.s_img_cur.func_name = func_name
#         self.s_img_cur.img_data = img_data
#         self.s_img_cur.gray_levels = gray_levels

class StateData:
    def __init__(self, image_id):
        self.s_img_ori_id = image_id
        self.s_img_cur_id = 0
        self.s_img_mask_id = 0
        self.s_img_hist_ids = []
        self.s_pointer = 1 #when delete old photo / push new photo need to update location of this pointer

    def get_ori_image(self): # may not need to pass image_id
        return UploadedImage.objects.get(pk=self.s_img_ori_id)

    def get_cur_image(self):
        return TempImage.objects.get(pk=self.s_img_cur_id)

    def get_temp_image_cv(self, image_id):
        temp_image = TempImage.objects.get(pk=image_id)
        return cv2.imread(temp_image.image.path)

    def get_cur_image_cv(self):
        cur_image = self.get_cur_image()
        return cv2.imread(cur_image.image.path)

    def get_ori_image_cv(self):
        ori_image = self.get_ori_image()
        return cv2.imread(ori_image.image.path)

    def get_temp_mask_cv(self, image_id):
        temp_image = TempImage.objects.get(pk=image_id)
        temp_mask = temp_image.mask
        print (temp_mask.mask.name)

        mask_cv = cv2.imread(temp_mask.mask.path)
        print("******max of mask cv", np.amax(mask_cv))
        return mask_cv

    def get_hist_thumbnail_cvs(self):
        thumbnail_cvs = []

        for img_hist_id in self.s_img_hist_ids:
            temp_image = TempImage.objects.get(pk=img_hist_id)
            thumbnail = temp_image.thumbnail
            thumbnail_cv = cv2.imread(thumbnail.path)
            thumbnail_cvs.append(thumbnail_cv)

        return thumbnail_cvs

    def get_hist_func_names(self):
        func_names = []

        for img_hist_id in self.s_img_hist_ids:
            temp_image = TempImage.objects.get(pk=img_hist_id)
            func_name = temp_image.func_name
            func_names.append(func_name)
        return func_names

    def pop_img_hist(self):
        img_hist_id = self.s_img_hist_ids.pop(0)
        temp_image = TempImage.objects.filter(pk=img_hist_id)
        temp_image.delete()

    def save_state(self):
        if len(self.s_img_hist_ids) >= MAX_UNDO_STEP:
           self.pop_img_hist()

        if len(self.s_img_hist_ids)==0:
            self.s_img_hist_ids.append(self.s_img_cur_id)
            self.s_pointer = len(self.s_img_hist_ids) -1
        else:
            # ! IMPORTANT: update: always keep the original image on top
            # remove the top - original image
            id = self.s_img_hist_ids.pop()
            # push current image id
            self.s_img_hist_ids.append(self.s_img_cur_id)
            # push back the original image id to top
            self.s_img_hist_ids.append(id)

            # current_state_img = StateImage(temp.s_img_cur.func_name, temp.s_img_cur.img_data, temp.s_img_cur.gray_levels)
            # temp.s_img_last_arr.append(current_state_img)
            # original_state_img = StateImage(temp.s_img_ori.func_name, temp.s_img_ori.img_data, temp.s_img_ori.gray_levels)
            # temp.s_img_last_arr.append(original_state_img)
            #
            # compressed_image = compress_image(copy.copy(temp.s_img_cur.img_data))
            # s_thumbnail_img = StateImage(temp.s_img_cur.func_name, compressed_image, temp.s_img_cur.gray_levels)
            # temp.s_thumb_hist_arr.append(s_thumbnail_img)
            #
            # compressed_ori_image = compress_image(copy.copy(temp.s_img_ori.img_data))
            # s_thumbnail_ori_img = StateImage(temp.s_img_ori.func_name, compressed_ori_image, temp.s_img_ori.gray_levels)
            # temp.s_thumb_hist_arr.append(s_thumbnail_ori_img)

            self.s_pointer = len(self.s_img_hist_ids) - 2 # ignore the original image on top
        print('pointer position', self.s_pointer)

    def reset(self):
        pass

# class StateImage:
#     def __init__(self, func_name, img_data, gray_levels=''):
#         self.func_name = func_name
#         self.img_data = img_data
#         self.gray_levels = gray_levels
#
#     def __repr__(self):
#         return "<Object func_name:%s gray_levels:%s>" % (self.func_name, self.gray_levels)
#

@timing
def get_state_data(temp_data_arr, image_id):
    return next((state_data for state_data in temp_data_arr if state_data.s_img_ori_id == image_id), None)

# if the image already had the state_data, replace it with fresh state_data
def new_state_data(temp_data_arr, image_id):
    # create a fresh temp object with userid and imageid
    state_data = get_state_data(temp_data_arr, image_id)
    if state_data is not None:
        temp_data_arr.remove(state_data)
    state_data = StateData(image_id)
    temp_data_arr.append(state_data)
    print("temp_data_arr", temp_data_arr)

    return state_data
    # return len(temp_data_arr)-1


# def get_temp_data(index, temp_data_arr):
#     i = int(index)
#     return temp_data_arr[i]



def update_state_data(state_data, func_name, image_cv, mask_data = None, func_setting='', gray_levels = [], k_labels = [], update_mask=False):
    temp_image = TempImage()
    temp_image_name = func_name + state_data.get_ori_image().image.name.split('/')[-1]

    temp_mask = TempMask()
    temp_mask.save(temp_image_name, mask_data)

    # temp_image.save(get_func_name(), img_data, get_func_name(), TempMask())

    temp_image.save(temp_image_name,
                    image_cv, func_name, temp_mask, func_setting, gray_levels, k_labels)
    state_data.s_img_cur_id = temp_image.id

    if update_mask:
        state_data.s_img_mask_id = temp_image.id
    # json_data, _ = cv_to_json(s_img_cur)
    state_data.save_state()


def get_thumbnail_plus_img_json(state_data):
    return thumbnail_plus_img_json(image_cv=state_data.get_cur_image_cv(), thumbnail_cvs=state_data.get_hist_thumbnail_cvs(),
                            func_names=state_data.get_hist_func_names(), func_name=state_data.get_cur_image().func_name,
                                   gray_levels=state_data.get_cur_image().gray_levels)