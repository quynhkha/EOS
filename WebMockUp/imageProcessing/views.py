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
original_image =np.zeros((400,400), np.uint8)
current_image = np.zeros((400,400), np.uint8)
current_mask = np.zeros((400,400), np.uint8)
last_state_image = np.zeros((400,400), np.uint8)
last_state_image_arr = []
history_thumbnail_arr = []
max_undo_steps = 6
undo_depth = 1
last_called_function = ""
labels = np.zeros((400, 400), np.uint8)

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
    return cv2.resize(image, (int(width/2), int(height/2)), interpolation=cv2.INTER_CUBIC)

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
            save_state_image()
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
    global history_thumbnail_arr
    global undo_depth
    if len(last_state_image_arr)>=max_undo_steps:
        last_state_image_arr.pop(0)
        history_thumbnail_arr.pop(0)

    last_state_image_arr.append(current_image)
    compressed_image = compress_image(copy.copy(current_image))
    history_thumbnail_arr.append(compressed_image)

    undo_depth = len(last_state_image_arr)-1
    print('undo depth', undo_depth)

def reset_current_image(function_name):
    global last_called_function
    global current_image
    if last_called_function == function_name:
        global last_state_image_arr
        global undo_depth
        current_image = last_state_image_arr[undo_depth]

    last_called_function = function_name
    undo_depth = len(last_state_image_arr) - 1
    print('undo depth', undo_depth)


# def save_second_last_state_image():
#     global last_state_image
#     global second_last_state_image
#     second_last_state_image = last_state_image

@csrf_exempt
def laplacian(request):
    global current_image
    #save_state_image()
    current_image = processingFunction.laplacian_func(current_image)
    #json_data, _ = cv_to_json(current_image)
    save_state_image()
    json_data = thumbnail_plus_img_json(current_image, history_thumbnail_arr)
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def kmeans(request):
    reset_current_image('kmeans')
    if request.method == 'POST':
        input = request.POST.get('input')
        print('input', input)
        input = int(input)
        global current_image
        #save_state_image()

        global original_image
        global labels
        current_image, labels = processingFunction.kmeans(current_image=current_image, segments=input)
        #json_data, _ = cv_to_json(current_image)
        save_state_image()
        json_data = thumbnail_plus_img_json(current_image, history_thumbnail_arr)
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
        global history_thumbnail_arr


        global original_image
        current_image = processingFunction.lower_thesholding(original_image=original_image, current_image=current_image, thresh_val=input)
        save_state_image()
        json_data = thumbnail_plus_img_json(current_image, history_thumbnail_arr)
        # json_data, _ = cv_to_json(current_image)
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
        #save_state_image()

        global original_image
        current_image = processingFunction.upper_thesholding(original_image=original_image, current_image=current_image, thresh_val=input)
        #json_data, _ = cv_to_json(current_image)
        save_state_image()
        json_data = thumbnail_plus_img_json(current_image, history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data})

@csrf_exempt
def undo_last_step(request):
    global current_image
    global last_state_image_arr
    global undo_depth

    if undo_depth>1:
        undo_depth -=1
    current_image = last_state_image_arr[undo_depth]
    print('undo depth', undo_depth)
    # json_data, _ = cv_to_json(current_image)
    # save_state_image()
    json_data = thumbnail_plus_img_json(current_image, history_thumbnail_arr)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def extract_crystal_mask(request):
    reset_current_image('extract_crystal_mask')
    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)
        global current_image
        #save_state_image()

        global original_image
        global labels
        current_image = processingFunction.extract_crystal_mask(current_image=current_image,
                                                        labels=labels, user_chosen_label=input)
        #json_data, _ = cv_to_json(current_image)
        save_state_image()
        global current_mask
        current_mask = current_image

        json_data = thumbnail_plus_img_json(current_image, history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data})

@csrf_exempt
def show_all_crystal(request):
    global current_image
    #save_state_image()

    global original_image
    current_image = processingFunction.show_all_crystal(original_image=original_image,
                                                        image_mask=current_image)
    #json_data, _ = cv_to_json(current_image)
    save_state_image()

    json_data = thumbnail_plus_img_json(current_image, history_thumbnail_arr)
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def show_max_area_crystal(request):
    global current_image
    global original_image
    current_image = processingFunction.show_top_area_crystals(original_image=original_image,
                                                              image_mask=current_image)

    save_state_image()
    json_data = thumbnail_plus_img_json(current_image, history_thumbnail_arr)
    # json_data, _ = cv_to_json(current_image)
    return JsonResponse(json_data)

@csrf_exempt
def reset(request):
    global current_image
    global original_image
    global history_thumbnail_arr
    global undo_depth
    global last_state_image_arr
    history_thumbnail_arr = []
    last_state_image_arr = []
    undo_depth = 0
    current_image = original_image
    save_state_image()

    json_data = thumbnail_plus_img_json(current_image, history_thumbnail_arr)
    return JsonResponse(json_data)

@csrf_exempt
def set_image_from_thumbnail(request):
    if request.method == 'POST':
        input = request.POST.get('input')
        thumbnail_id = str(input)
        id = int(thumbnail_id.split("_")[1])
        global current_image
        #save_state_image()

        global original_image
        global last_state_image_arr
        global undo_depth

        current_image = last_state_image_arr[id]
        undo_depth = input
        json_data = thumbnail_plus_img_json(current_image, history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data})

@csrf_exempt
def plot_histogram(request):
    global current_image
    global current_mask
    hist_y_axis, hist_x_axis = processingFunction.plot_histogram(current_image, current_mask)
    json_data = {'x': hist_x_axis.tolist(), 'y': hist_y_axis.tolist()}
    return JsonResponse(json_data)

@csrf_exempt
def do_opening(request):
    reset_current_image('do_opening')
    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))
        global current_image
        global current_mask

        current_image = processingFunction.opening(current_image, kernel_size, num_of_iter)
        # save_state_image()
        current_mask = current_image

        json_data = thumbnail_plus_img_json(current_image, history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data':image_data})


@csrf_exempt
def do_closing(request):
    reset_current_image('do_closing')
    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))
        global current_image
        global current_mask

        current_image = processingFunction.closing(current_image, kernel_size, num_of_iter)
        # save_state_image()
        current_mask = current_image

        json_data = thumbnail_plus_img_json(current_image, history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data':image_data})



@csrf_exempt
def do_erosion(request):
    reset_current_image('do_erosion')
    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))
        global current_image
        global current_mask

        current_image = processingFunction.erosion(current_image, kernel_size, num_of_iter)
        # save_state_image()
        current_mask = current_image

        json_data = thumbnail_plus_img_json(current_image, history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data':image_data})



@csrf_exempt
def do_dilation(request):
    reset_current_image('do_dilation')
    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))
        global current_image
        global current_mask

        current_image = processingFunction.dilation(current_image, kernel_size, num_of_iter)
        # save_state_image()
        current_mask = current_image

        json_data = thumbnail_plus_img_json(current_image, history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(current_image)
    return render(request, 'imageProcessing/processing_page.html', {'image_data':image_data})