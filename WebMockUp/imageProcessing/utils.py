import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class findImageDir:
    def __init__(self):
        return

    def imageDirfromImg(self, image):
        imageURL = image.imageData.url
        imageDir = str(BASE_DIR) + str(imageURL)
        return imageDir

    def folderDirfromImg(self, image):
        imageDir = self.imageDirfromImg(image)
        imageFileName = os.path.splitext(imageDir)[0]
        #print (imageFileName)
        mediaDir = os.path.join(BASE_DIR, 'media')
        folderDir = os.path.join(mediaDir, imageFileName)
        return folderDir

    def imageDirfromImgURL(self, imageURL):
        imageDir = str(BASE_DIR) + str(imageURL)
        return imageDir

    def folderDirfromImgURL(self, imageURL):
        imageFileName = os.path.splitext(imageURL)[0]
        # print (imageFileName)
        mediaDir = os.path.join(BASE_DIR, 'media')
        folderDir = os.path.join(mediaDir, imageFileName)
        return folderDir
