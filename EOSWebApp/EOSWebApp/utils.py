import base64
import inspect
import time

import numpy as np

from EOSWebApp.settings import PROJECT_ROOT

IMAGE_URL = '/media/images/'
THUMBNAIL_URL = '/media/thumbnails/'
CRYSTAL_MASK_URL = '/media/masks/'
CRYSTAL_URL = '/media/crystals/'
TEMP_DIR = '/home/long/EOSImages/'
PERFORMANCE_TEST = True

class SharedData:
    def __init__(self):
        self.temp_data_arr = []

shared_data = SharedData()


from PIL import Image
import cv2
from io import BytesIO


def timing(f):
    def wrap(*args, **kw):
        time1 = time.time()
        ret = f(*args, **kw)
        time2 = time.time()
        if PERFORMANCE_TEST:
            print('%s function took %0.3f ms' % (f.__name__, (time2 - time1) * 1000.0))
        return ret

    return wrap


@timing
def cv_to_bytesIO(cv_image, format = "JPEG"):
    if len(cv_image.shape) == 3:
        pil_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    else:
        pil_image = cv_image
    bytes_io = BytesIO()
    pil_image = Image.fromarray(pil_image)
    pil_image.save(bytes_io, format=format)

    return bytes_io


@timing
def cv_to_json(image, is_state_img=True):
    # img_file = open("/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.small.png", "rb")
    # img = img_file.read()
    # opencv_img = cv2.imread('/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.tif')
    # if is_state_img:
    #     opencv_img = image.img_data
    # else:
    #     opencv_img = image
    opencv_img = image
    retval, img = cv2.imencode('.jpg', opencv_img)
    base64_bytes = base64.b64encode(img)
    base64_string = base64_bytes.decode('utf8')
    # if is_state_img:
    #     json_data = {'image_data': base64_string, 'func_name': image.func_name}
    # else:
    json_data = {'image_data': base64_string}
    return json_data, base64_string


def json_to_cv(json_img):
    # encoded_data = json_img.split(',')[1]
    # np_data = np.fromstring(encoded_data.decode('base64'), np.unit8)
    data_img = json_img.split('data:image/jpeg;base64,')[1]

    utf8_img = data_img.encode('utf8')
    encoded_data = base64.b64decode(utf8_img)
    # img = cv2.imdecode('.jpg', encoded_data)
    np_data = np.fromstring(encoded_data, np.uint8)
    img = cv2.imdecode(np_data, 1)
    return img


@timing
def thumbnail_plus_img_json(image_cv, thumbnail_cvs, func_names):
    thumbnail_arr_base64 = []
    thumbnail_arr_func_name = []
    _, base64_image = cv_to_json(image_cv)

    for thumbnail_cv in thumbnail_cvs:
        _, thumbnail_base64 = cv_to_json(thumbnail_cv)
        thumbnail_arr_base64.append(thumbnail_base64)

    for func_name in func_names:
        thumbnail_arr_func_name.append(func_name)

    json_data = {'image_data': base64_image, 'func_name': '', 'gray_levels': '',
                 'thumbnail_arr': thumbnail_arr_base64, 'thumb_func_name': thumbnail_arr_func_name}
    return json_data


def absolute_file_dir(filename, target_url):
    return str(PROJECT_ROOT) + target_url + filename


def compress_image(image, mod_size=0):
    if len(image.shape) == 3:
        (height, width, _) = image.shape
    else:
        (height, width) = image.shape
    if mod_size == 0:
        if width <= 800:
            resize_factor = 4
        elif width <= 1600:
            resize_factor = 8
        else:
            resize_factor = 16
    else:
        resize_factor = mod_size
    return cv2.resize(image, (int(width / resize_factor), int(height / resize_factor)), interpolation=cv2.INTER_CUBIC)


def get_func_name():
    # frame = inspect.currentframe()
    # return inspect.getframeinfo(frame).function
    return inspect.stack()[1][3]