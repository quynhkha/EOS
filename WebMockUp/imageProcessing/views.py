from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from imageProcessing.FindSegment import FindSegment
from .forms import NameForm, PostForm
from .models import Image
from .utils import findImageDir

findDir = findImageDir()
findSegment = FindSegment()
processedImageURL =""
db_image_dir = ""

# Create your views here.
def showImage(request, image_id):
    db_image = get_object_or_404(Image, pk=image_id)
    return render(request, 'imageProcessing/imageProcessing.html', {'image': db_image})

def masking(request):
    db_image = get_object_or_404(Image, pk=2)
    global db_image_dir
    db_image_dir = findDir.imageDirfromDatabaseImg(db_image)

    image_copy_dir = findSegment.save_an_image_copy(db_image, db_image_dir)
    print('imageDir: ', db_image_dir, 'image_copy_dir', image_copy_dir)

    global processedImageURL
    processedImageURL= findSegment.imageMasking(image_copy_dir, 5)
    print("processedImageURL: ", processedImageURL)
    return HttpResponse(processedImageURL)

def dilating(request):
    global processedImageURL
    print("processedImageURL", processedImageURL)

    processed_image_dir = findDir.imageDirfromImgURL(processedImageURL)
    processedImageURL = findSegment.imageDilate(processed_image_dir, 3)

    return HttpResponse(processedImageURL)

def pengzhang(request):
    global processedImageURL
    global db_image_dir
    print("processedImageURL", processedImageURL)

    processed_image_dir= findDir.imageDirfromImgURL(processedImageURL)
    processedImageURL = findSegment.imagePengzhang(db_image_dir, processed_image_dir)

    return HttpResponse(processedImageURL)

def windowing(request):
    global processedImageURL
    print("processedImageURL", processedImageURL)

    processed_image_dir = findDir.imageDirfromImgURL(processedImageURL)
    processedImageURL = findSegment.imageWindowing(processed_image_dir, 20)

    return HttpResponse(processedImageURL)

def ostu(request):
    global processedImageURL
    print("processedImageURL", processedImageURL)

    processed_image_dir = findDir.imageDirfromImgURL(processedImageURL)
    processedImageURL = findSegment.imageOstu(processed_image_dir, 8)

    return HttpResponse(processedImageURL)

def success_message(request):
    return render (request, 'imageProcessing/thankMessage.html')

def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data)
            return HttpResponseRedirect('/imageProcessing/success/')
        else:
            form = NameForm()
        return render(request, 'imageProcessing/your_name.html', {'form': form})

def post_new(request):
    form = PostForm()
    return render (request, 'imageProcessing/post_edit.html', {'form': form})
