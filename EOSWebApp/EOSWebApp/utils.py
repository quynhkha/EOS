from EOSWebApp.imageProcessing.utils import timing

IMAGE_URL = '/media/images/'
THUMBNAIL_URL = '/media/thumbnails/'
CRYSTAL_MASK_URL = '/media/masks/'
CRYSTAL_URL = '/media/crystals/'
TEMP_DIR = '/home/long/EOSImages/'

class SharedData:
    def __init__(self):
        self.temp_data_arr = []

shared_data = SharedData()


from PIL import Image
import cv2
from io import BytesIO

@timing
def cv_to_bytesIO(cv_image):
    rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    bytes_io = BytesIO()
    pil_image = Image.fromarray(rgb_image)
    pil_image.save(bytes_io, format="JPEG")

    return bytes_io

