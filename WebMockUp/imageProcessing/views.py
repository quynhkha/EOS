import base64
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from imageProcessing.FindSegment import FindSegment
from .forms import *
from .models import Image
from .utils import *

import copy
import cv2
from django.http import JsonResponse
from .forms import UploadFileForm
from django.views.decorators.csrf import csrf_exempt
from .imageProcessingFunc.crystal_extractor import ProcessingFunction


processingFunction = ProcessingFunction()
# tempData = TempData()
tempDataArr = []
tempIndex = 0

def newTempData():
    tempData = TempData()
    tempDataArr.append(tempData)
    return len(tempDataArr)-1

def getTempData(index):
    i = int(index)
    return tempDataArr[i]

# for testing purpose only
def show_base64(request):
    opencv_img = cv2.imread('/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.small.png')
    json_data, _= cv_to_json(opencv_img)
    return JsonResponse(json_data, safe=False)

def compress_image(image):
    if len(image.shape) == 3:
        (height, width, _) =image.shape
    else:
        (height, width) = image.shape
    return cv2.resize(image, (int(width/4), int(height/4)), interpolation=cv2.INTER_CUBIC)

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

            global tempIndex
            tempIndex = newTempData()
            temp = getTempData(tempIndex)

            temp.original_image = cv2.imread(image_file_dir)
            temp.current_image=temp.original_image
            save_state_image(tempIndex)
            _, image_data = cv_to_json(temp.original_image)
            return render(request, 'imageProcessing/processing_page.html', {'image_data':image_data, 'temp_index':tempIndex})
    else:
        form = DocumentForm()
    return render(request, 'imageProcessing/model_form_upload.html', {'form': form})

def save_state_image(tempIndex):
    # global current_image
    # global last_state_image
    # last_state_image = current_image
    # save_second_last_state_image()

    temp = getTempData(tempIndex)
    if len(temp.last_state_image_arr)>=temp.max_undo_steps:
        temp.last_state_image_arr.pop(0)
        temp.history_thumbnail_arr.pop(0)

    temp.last_state_image_arr.append(temp.current_image)
    compressed_image = compress_image(copy.copy(temp.current_image))
    temp.history_thumbnail_arr.append(compressed_image)

    temp.undo_depth = len(temp.last_state_image_arr)-1
    print('undo depth', temp.undo_depth)

def reset_current_image(function_name, tempIndex):

    temp = getTempData(tempIndex)
    if temp.last_called_function == function_name:
        temp.current_image = temp.last_state_image_arr[temp.undo_depth]

    temp.last_called_function = function_name
    temp.undo_depth = len(temp.last_state_image_arr) - 1
    print('undo depth', temp.undo_depth)


# def save_second_last_state_image():
#     global last_state_image
#     global second_last_state_image
#     second_last_state_image = last_state_image

@csrf_exempt
def laplacian(request, tempIndex=0):
    temp = getTempData(tempIndex)
    #save_state_image()
    temp.current_image = processingFunction.laplacian_func(temp.current_image)
    #json_data, _ = cv_to_json(current_image)
    save_state_image(tempIndex)
    json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def kmeans(request, tempIndex=0):
    temp = getTempData(tempIndex)
    reset_current_image('kmeans', tempIndex)

    if request.method == 'POST':
        input = request.POST.get('input')
        print('input', input)
        input = int(input)

        temp.current_image, temp.labels = processingFunction.kmeans(current_image=temp.current_image, segments=input)
        #json_data, _ = cv_to_json(current_image)
        save_state_image(tempIndex)
        json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.current_image)
    return render(request, 'imageProcessing/processing_page.html',
                      {'image_data': image_data, 'temp_index': tempIndex})

@csrf_exempt
def lower_thresholding(request, tempIndex=0):

    temp = getTempData(tempIndex)
    reset_current_image('lower_thesholding',tempIndex)
    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)

        temp.current_image = processingFunction.lower_thesholding(original_image=temp.original_image, current_image=temp.current_image, thresh_val=input)
        save_state_image(tempIndex)
        json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
        # json_data, _ = cv_to_json(current_image)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.current_image)
    return render(request, 'imageProcessing/processing_page.html',
                      {'image_data': image_data, 'temp_index': tempIndex})

@csrf_exempt
def upper_thresholding(request, tempIndex=0):
    reset_current_image('upper_theshoding', tempIndex)
    temp = getTempData(tempIndex)
    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)

        temp.current_image = processingFunction.upper_thesholding(original_image=temp.original_image, current_image=temp.current_image, thresh_val=input)
        #json_data, _ = cv_to_json(current_image)
        save_state_image(tempIndex)
        json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': tempIndex})

@csrf_exempt
def undo_last_step(request, tempIndex=0):
    temp = getTempData(tempIndex)

    if temp.undo_depth>1:
        temp.undo_depth -=1
    temp.current_image = temp.last_state_image_arr[temp.undo_depth]
    print('undo depth', temp.undo_depth)
    # json_data, _ = cv_to_json(current_image)
    # save_state_image()
    json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def extract_crystal_mask(request, tempIndex=0):
    reset_current_image('extract_crystal_mask', tempIndex)
    temp = getTempData(tempIndex)

    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)

        temp.current_image = processingFunction.extract_crystal_mask(current_image=temp.current_image,
                                                        labels=temp.labels, user_chosen_label=input)
        #json_data, _ = cv_to_json(current_image)
        save_state_image(tempIndex)

        temp.current_mask = temp.current_image

        json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.current_image)
    return render(request, 'imageProcessing/processing_page.html',
                      {'image_data': image_data, 'temp_index': tempIndex})

@csrf_exempt
def show_all_crystal(request, tempIndex=0):
    temp = getTempData(tempIndex)

    temp.current_image = processingFunction.show_all_crystal(original_image=temp.original_image,
                                                        image_mask=temp.current_image)
    #json_data, _ = cv_to_json(current_image)
    save_state_image(tempIndex)

    json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def show_top_area_crystal(request, tempIndex=0):
    temp = getTempData(tempIndex)

    num_of_crystals = int(request.POST.get('input'))

    temp.current_image = processingFunction.show_top_area_crystals(original_image=temp.original_image,
                                                              image_mask=temp.current_image, num_of_crystals=num_of_crystals)

    save_state_image(tempIndex)
    json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
    # json_data, _ = cv_to_json(current_image)
    return JsonResponse(json_data)

@csrf_exempt
def reset(request, tempIndex=0):
    temp = getTempData(tempIndex)

    temp.history_thumbnail_arr = []
    temp.last_state_image_arr = []
    temp.undo_depth = 0
    temp.current_image = temp.original_image

    save_state_image(tempIndex)

    json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
    return JsonResponse(json_data)

@csrf_exempt
def set_image_from_thumbnail(request, tempIndex=0):
    temp = getTempData(tempIndex)

    if request.method == 'POST':
        input = request.POST.get('input')
        thumbnail_id = str(input)
        id = int(thumbnail_id.split("_")[1])

        temp.current_image = temp.last_state_image_arr[id]
        temp.undo_depth = input
        json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.current_image)
    return render(request, 'imageProcessing/processing_page.html',
                      {'image_data': image_data, 'temp_index': tempIndex})

@csrf_exempt
def plot_histogram(request, tempIndex=0):
    temp = getTempData(tempIndex)

    hist_y_axis, hist_x_axis = processingFunction.plot_histogram(temp.current_image, temp.current_mask)
    json_data = {'x': hist_x_axis.tolist(), 'y': hist_y_axis.tolist()}
    return JsonResponse(json_data)

@csrf_exempt
def do_opening(request, tempIndex=0):
    reset_current_image('do_opening', tempIndex)
    temp = getTempData(tempIndex)
    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        temp.current_image = processingFunction.opening(temp.current_image, kernel_size, num_of_iter)
        # save_state_image()
        temp.current_mask = temp.current_image

        json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': tempIndex})


@csrf_exempt
def do_closing(request, tempIndex=0):
    reset_current_image('do_closing', tempIndex)
    temp = getTempData(tempIndex)

    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        temp.current_image = processingFunction.closing(temp.current_image, kernel_size, num_of_iter)
        # save_state_image()
        temp.current_mask = temp.current_image

        json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': tempIndex})



@csrf_exempt
def do_erosion(request, tempIndex=0):
    reset_current_image('do_erosion', tempIndex)
    temp = getTempData(tempIndex)

    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        temp.current_image = processingFunction.erosion(temp.current_image, kernel_size, num_of_iter)
        # save_state_image()
        temp.current_mask = temp.current_image

        json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': tempIndex})


@csrf_exempt
def do_dilation(request, tempIndex=0):
    reset_current_image('do_dilation', tempIndex)
    temp = getTempData(tempIndex)

    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        temp.current_image = processingFunction.dilation(temp.current_image, kernel_size, num_of_iter)
        # save_state_image()
        temp.current_mask = temp.current_image

        json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': tempIndex})

@csrf_exempt
def update_mask(request, tempIndex=0):
    if request.method == 'POST':
        rgb_mask_data = request.POST.get('mask')
        rgb_mask = json_to_cv(rgb_mask_data)

        temp = getTempData(tempIndex)

        temp.current_image, temp.current_mask = processingFunction.handle_mask(rgb_mask, temp.current_mask, temp.original_image)


        # current_image = processingFunction.show_all_crystal(original_image=original_image,
        #                                                     image_mask=current_mask)
        # json_data, _ = cv_to_json(current_image)
        save_state_image(tempIndex)

        json_data = thumbnail_plus_img_json(temp.current_image, temp.history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
        # json_data = thumbnail_plus_img_json(mask, history_thumbnail_arr)
        # return JsonResponse(json_data, safe=False)

