import base64
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from imageProcessing.FindSegment import FindSegment
from .forms import *
from .models import Image
from .utils import *

import cv2
from django.http import JsonResponse
from .forms import UploadFileForm
from django.views.decorators.csrf import csrf_exempt
from .imageProcessingFunc.crystal_extractor import ProcessingFunction


#
# findDir = findImageDir()
# findSegment = FindSegment()
# processedImageURL =""
# db_image_dir = ""

# # Create your views here.
# def showImage(request, image_id):
#     db_image = get_object_or_404(Image, pk=image_id)
#     return render(request, 'imageProcessing/imageProcessing.html', {'image': db_image})
#
# def masking(request):
#     db_image = get_object_or_404(Image, pk=2)
#     global db_image_dir
#     db_image_dir = findDir.imageDirfromDatabaseImg(db_image)
#
#     image_copy_dir = findSegment.save_an_image_copy(db_image, db_image_dir)
#     print('imageDir: ', db_image_dir, 'image_copy_dir', image_copy_dir)
#
#     global processedImageURL
#     processedImageURL= findSegment.imageMasking(image_copy_dir, 5)
#     print("processedImageURL: ", processedImageURL)
#     return HttpResponse(processedImageURL)
#
# def dilating(request):
#     global processedImageURL
#     print("processedImageURL", processedImageURL)
#
#     processed_image_dir = findDir.imageDirfromImgURL(processedImageURL)
#     processedImageURL = findSegment.imageDilate(processed_image_dir, 3)
#
#     return HttpResponse(processedImageURL)
#
# def pengzhang(request):
#     global processedImageURL
#     global db_image_dir
#     print("processedImageURL", processedImageURL)
#
#     processed_image_dir= findDir.imageDirfromImgURL(processedImageURL)
#     processedImageURL = findSegment.imagePengzhang(db_image_dir, processed_image_dir)
#
#     return HttpResponse(processedImageURL)
#
# def windowing(request):
#     global processedImageURL
#     print("processedImageURL", processedImageURL)
#
#     processed_image_dir = findDir.imageDirfromImgURL(processedImageURL)
#     processedImageURL = findSegment.imageWindowing(processed_image_dir, 20)
#
#     return HttpResponse(processedImageURL)
#
# def ostu(request):
#     global processedImageURL
#     print("processedImageURL", processedImageURL)
#
#     processed_image_dir = findDir.imageDirfromImgURL(processedImageURL)
#     processedImageURL = findSegment.imageOstu(processed_image_dir, 8)
#
#     return HttpResponse(processedImageURL)
#
# def success_message(request):
#     return render (request, 'imageProcessing/thankMessage.html')
#
# def get_name(request):
#     if request.method == 'POST':
#         form = NameForm(request.POST)
#
#         if form.is_valid():
#             print(form.cleaned_data)
#             return HttpResponseRedirect('/imageProcessing/success/')
#         else:
#             form = NameForm()
#         return render(request, 'imageProcessing/your_name.html', {'form': form})
#
# def post_new(request):
#     form = PostForm()
#     return render (request, 'imageProcessing/post_edit.html', {'form': form})

processingFunction = ProcessingFunction()
original_image =np.zeros((400,400), np.uint8)
current_image = np.zeros((400,400), np.uint8)
last_state_image = np.zeros((400,400), np.uint8)
last_state_image_arr = []
last_state_image_arr_size = 5
undo_depth = 0
last_called_function = ""
labels = np.zeros((400, 400), np.uint8)

def show_base64(request):
    opencv_img = cv2.imread('/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.small.png')
    json_data, _= cv_to_json(opencv_img)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            file= request.FILES['document']
            print("filename", file.name, "file content type", file.content_type, "file size", file.size)
            image_file_dir = absolute_uploaded_file_dir(file.name)
            print ("image file dir", image_file_dir)
            global original_image
            global current_image
            original_image = cv2.imread(image_file_dir)
            current_image=original_image
            _, image_data = cv_to_json(original_image)
            return render(request, 'imageProcessing/processing_page.html', {'image_data':image_data })
    else:
        form = DocumentForm()
    return render(request, 'imageProcessing/model_form_upload.html', {'form': form})

def save_state_image():
    # global current_image
    # global last_state_image
    # last_state_image = current_image
    # save_second_last_state_image()
    global current_image
    global last_state_image_arr
    global undo_depth
    if len(last_state_image_arr)>=last_state_image_arr_size:
        last_state_image_arr.pop(0)

    last_state_image_arr.append(current_image)
    undo_depth = len(last_state_image_arr)-1

def reset_current_image(function_name):
    global last_called_function
    global current_image
    if last_called_function == function_name:
        global last_state_image_arr
        global undo_depth
        current_image = last_state_image_arr[undo_depth]

    last_called_function = function_name


# def save_second_last_state_image():
#     global last_state_image
#     global second_last_state_image
#     second_last_state_image = last_state_image

@csrf_exempt
def laplacian(request):
    global current_image
    save_state_image()
    current_image = processingFunction.laplacian_func(current_image)
    json_data, _ = cv_to_json(current_image)
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def kmeans(request):
    reset_current_image('kmeans')
    if request.method == 'POST':
        input = request.POST.get('input')
        print('input', input)
        input = int(input)
        global current_image
        save_state_image()

        global original_image
        global labels
        current_image, labels = processingFunction.kmeans(current_image=current_image, segments=input)
        json_data, _ = cv_to_json(current_image)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data})

@csrf_exempt
def lower_thresholding(request):

    reset_current_image('lower_thesholding')
    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)
        global current_image
        save_state_image()

        global original_image
        current_image = processingFunction.lower_thesholding(original_image=original_image, current_image=current_image, thresh_val=input)
        json_data, _ = cv_to_json(current_image)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data})

@csrf_exempt
def upper_thresholding(request):
    reset_current_image('upper_theshoding')
    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)
        global current_image
        save_state_image()

        global original_image
        current_image = processingFunction.upper_thesholding(original_image=original_image, current_image=current_image, thresh_val=input)
        json_data, _ = cv_to_json(current_image)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data})

@csrf_exempt
def undo_last_step(request):
    global current_image
    global last_state_image_arr
    global undo_depth
    current_image = last_state_image_arr[undo_depth]
    if undo_depth>0:
        undo_depth -=1

    json_data, _ = cv_to_json(current_image)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def extract_crystal_mask(request):
    reset_current_image('extract_crystal_mask')
    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)
        global current_image
        save_state_image()

        global original_image
        global labels
        current_image = processingFunction.extract_crystal_mask(current_image=current_image,
                                                        labels=labels, user_chosen_label=input)
        json_data, _ = cv_to_json(current_image)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data})

@csrf_exempt
def show_all_crystal(request):
    global current_image
    save_state_image()

    global original_image
    current_image = processingFunction.show_all_crystal(original_image=original_image,
                                                        image_mask=current_image)
    json_data, _ = cv_to_json(current_image)
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def show_max_area_crystal(request):
    global current_image
    save_state_image()

    global original_image
    current_image = processingFunction.show_max_area_crystal(original_image=original_image,
                                                             image_mask=current_image)
    json_data, _ = cv_to_json(current_image)
    return JsonResponse(json_data, safe=False)