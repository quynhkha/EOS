from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Image
from .imageProcessingFunc.FindSegment import FindSegment
from .utils import findImageDir

findDir = findImageDir()
findSegment = FindSegment()
processedImageURL =""

# Create your views here.
def showImage(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    return render(request, 'imageProcessing/imageProcessing.html', {'image': image})

def masking(request):
    image = get_object_or_404(Image, pk=1)
    imageDir = findDir.imageDirfromImg(image)
    folderDir = findDir.folderDirfromImg(image)
    # findSegment.makeDir(folderDir)

    global processedImageURL
    processedImageURL= findSegment.imageMasking(imageDir, folderDir, 5)
    return HttpResponse(processedImageURL)

def dilating (request):
    global processedImageURL
    print (processedImageURL)
    imageDir = findDir.imageDirfromImgURL(processedImageURL)
    folderDir = findDir.folderDirfromImgURL(processedImageURL)
    print(imageDir, folderDir)
    processedImageURL = findSegment.imageDilate(imageDir, folderDir, 3)
    return HttpResponse(processedImageURL)