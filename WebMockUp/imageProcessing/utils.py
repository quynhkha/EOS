import os

import PIL
import numpy as np
import cv2
import base64

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

def cv_to_json(opencv_img):
    # img_file = open("/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.small.png", "rb")
    # img = img_file.read()
    #opencv_img = cv2.imread('/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.tif')
    retval, img = cv2.imencode('.jpg', opencv_img)
    base64_bytes = base64.b64encode(img)
    base64_string = base64_bytes.decode('utf8')
    json_data = {'image_data': base64_string}
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

def thumbnail_plus_img_json(image, thumbnail_arr):
    base64_thumbnail_arr = []
    _, base64_image = cv_to_json(image)
    for thumbnail in thumbnail_arr:
        _, base64_thumbnail = cv_to_json(thumbnail)
        base64_thumbnail_arr.append(base64_thumbnail)
    json_data = {'image_data': base64_image, 'thumbnail_arr': base64_thumbnail_arr}
    return json_data

def absolute_uploaded_file_dir(filename):
    return str(BASE_DIR)+'/media/documents/'+filename