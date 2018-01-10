import copy
import os

import PIL
import numpy as np
import cv2
import base64

import time


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PERFORMANCE_TEST = False

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        if PERFORMANCE_TEST:
            print ('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap

@timing
def cv_to_json(opencv_state_img):
    # img_file = open("/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.small.png", "rb")
    # img = img_file.read()
    #opencv_img = cv2.imread('/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.tif')
    opencv_img = opencv_state_img.img_data
    retval, img = cv2.imencode('.jpg', opencv_img)
    base64_bytes = base64.b64encode(img)
    base64_string = base64_bytes.decode('utf8')
    json_data = {'image_data': base64_string, 'func_name': opencv_state_img.func_name}
    return json_data, base64_string

def json_to_cv(json_img):
    # encoded_data = json_img.split(',')[1]
    # np_data = np.fromstring(encoded_data.decode('base64'), np.unit8)
    data_img = json_img.split('data:image/jpeg;base64,')[1]

    utf8_img =data_img.encode('utf8')
    encoded_data = base64.b64decode(utf8_img)
    # img = cv2.imdecode('.jpg', encoded_data)
    np_data = np.fromstring(encoded_data, np.uint8)
    img = cv2.imdecode(np_data, 1)
    return img

@timing
def thumbnail_plus_img_json(state_image, state_thumbnail_arr):
    thumbnail_arr_base64 = []
    thumbnail_arr_func_name = []
    _, base64_image = cv_to_json(state_image)
    for state_thumbnail in state_thumbnail_arr:
        _, base64_thumbnail = cv_to_json(state_thumbnail)
        thumbnail_arr_base64.append(base64_thumbnail)
        thumbnail_arr_func_name.append(state_thumbnail.func_name)

    json_data = {'image_data': base64_image, 'func_name': state_image.func_name, 'gray_levels': state_image.gray_levels,
                 'thumbnail_arr': thumbnail_arr_base64, 'thumb_func_name': thumbnail_arr_func_name}
    return json_data

def absolute_file_dir(filename, target_url):
    return str(BASE_DIR) + target_url + filename

# def absolute_uploaded_file_dir(url):
#      return str(BASE_DIR)+url

def compress_image(image):
    if len(image.shape) == 3:
        (height, width, _) =image.shape
    else:
        (height, width) = image.shape
    if width <= 800:
        resize_factor = 4
    elif width <= 1600:
        resize_factor = 8
    else:
        resize_factor = 16
    return cv2.resize(image, (int(width/resize_factor), int(height/resize_factor)), interpolation=cv2.INTER_CUBIC)


def new_temp_data(temp_data_arr, user_id, image_id):
    # create a fresh temp object with userid and imageid
    tempData = get_temp_data(temp_data_arr, user_id, image_id)
    if tempData is not None:
        temp_data_arr.remove(tempData)
    tempData = TempData()
    tempData.user_id = user_id
    tempData.image_id = image_id
    temp_data_arr.append(tempData)
    print("temp_data_arr", temp_data_arr)
    return tempData
    # return len(temp_data_arr)-1


# def get_temp_data(index, temp_data_arr):
#     i = int(index)
#     return temp_data_arr[i]

def get_temp_data(temp_data_arr, user_id, image_id):
    return next((temp for temp in temp_data_arr if temp.user_id == user_id and temp.image_id == image_id), None)
# append the current image to saved image arr and thumbnail arr

# def save_state(temp_idx, temp_data_arr):
#
#     temp = get_temp_data(temp_idx, temp_data_arr)
#     if len(temp.s_img_last_arr)>=temp.s_max_undo_step:
#         temp.s_img_last_arr.pop(0)
#         temp.s_thumb_hist_arr.pop(0)
#
#     current_state_img = StateImage(temp.s_img_cur.func_name, temp.s_img_cur.img_data, temp.s_img_cur.gray_levels)
#     temp.s_img_last_arr.append(current_state_img)
#
#     compressed_image = compress_image(copy.copy(temp.s_img_cur.img_data))
#     s_thumbnail_img = StateImage(temp.s_img_cur.func_name, compressed_image, temp.s_img_cur.gray_levels)
#     temp.s_thumb_hist_arr.append(s_thumbnail_img)
#
#     temp.s_undo_depth = len(temp.s_img_last_arr)-1
#     print('undo depth', temp.s_undo_depth)

def save_state(temp):

    if len(temp.s_img_last_arr)>=temp.s_max_undo_step:
        temp.s_img_last_arr.pop(0)
        temp.s_thumb_hist_arr.pop(0)

    current_state_img = StateImage(temp.s_img_cur.func_name, temp.s_img_cur.img_data, temp.s_img_cur.gray_levels)
    temp.s_img_last_arr.append(current_state_img)

    compressed_image = compress_image(copy.copy(temp.s_img_cur.img_data))
    s_thumbnail_img = StateImage(temp.s_img_cur.func_name, compressed_image, temp.s_img_cur.gray_levels)
    temp.s_thumb_hist_arr.append(s_thumbnail_img)

    temp.s_undo_depth = len(temp.s_img_last_arr)-1
    print('undo depth', temp.s_undo_depth)


def reset_current_image(func_name, temp_idx, temp_data_arr):

    temp = get_temp_data(temp_idx, temp_data_arr)
    if temp.s_just_recovered == True:
        if temp.s_last_cal_func == func_name:
            temp.s_img_cur = copy.copy(temp.s_img_last_arr[temp.s_undo_depth])
        temp.s_just_recovered = False

    temp.s_last_cal_func = func_name
    temp.s_undo_depth = len(temp.s_img_last_arr) - 1
    print('undo depth', temp.s_undo_depth)

# from django.contrib.auth.models import User
# users = User.objects.all()
# print(users.values_list('password', flat=True))

class TempData:
    def __init__(self):
        self.s_img_ori= StateImage('original image', np.zeros((400, 400), np.uint8))
        self.s_img_cur = StateImage('current image', np.zeros((400, 400), np.uint8))
        self.s_mask_cur = StateImage('current mask', np.zeros((400, 400), np.uint8))
        self.s_img_last = StateImage('last image', np.zeros((400, 400), np.uint8))
        self.s_img_last_arr = []
        self.s_thumb_hist_arr = []
        self.s_max_undo_step = 10
        self.s_undo_depth = 1
        self.s_last_cal_func = ""
        self.s_labels = 0
        self.s_just_recovered = False
        self.user_id = ''
        self.image_id = ''

    def update_s_img_cur(self, func_name, img_data, gray_levels=''):
        self.s_img_cur.func_name = func_name
        self.s_img_cur.img_data = img_data
        self.s_img_cur.gray_levels = gray_levels

class StateImage:
    def __init__(self, func_name, img_data, gray_levels=''):
        self.func_name = func_name
        self.img_data = img_data
        self.gray_levels = gray_levels

    def __repr__(self):
        return "<Object func_name:%s gray_levels:%s>" % (self.func_name, self.gray_levels)

class findImageDir:
    def __init__(self):
        return


    def imageDirfromDatabaseImg(self, image):
        imageURL = image.imageData.url
        imageDir = str(BASE_DIR) + str(imageURL)
        return imageDir

    # def folderDirfromDatabaseImg(self, image):
    #     imageDir = self.imageDirfromDatabaseImg(image)
    #     imageFileName = os.path.splitext(imageDir)[0]
    #     #print (imageFileName)
    #     mediaDir = os.path.join(BASE_DIR, 'media')
    #     folderDir = os.path.join(mediaDir, imageFileName)
    #     return folderDir

    def imageDirfromImgURL(self, imageURL):
        imageDir = str(BASE_DIR) + str(imageURL)
        return imageDir

    # def folderDirfromImgURL(self, imageURL):
    #     imageFileName = os.path.splitext(imageURL)[0]
    #     # print (imageFileName)
    #     mediaDir = os.path.join(BASE_DIR, 'media')
    #     folderDir = os.path.join(mediaDir, imageFileName)
    #     return folderDir

# class image_maipulation:
#     def __init__(self):
#         return
#
#     def saveImage(self, image_model):
#         imageDir
#         image = np.asarray(PIL.Image.open(imageDir))