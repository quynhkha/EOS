IMAGE_URL = '/media/images/'
THUMBNAIL_URL = '/media/thumbnails/'
CRYSTAL_MASK_URL = '/media/masks/'
CRYSTAL_URL = '/media/crystals/'
TEMP_DIR = '/home/long/EOSImages/'

class SharedData:
    def __init__(self):
        self.temp_data_arr = []

shared_data = SharedData()
