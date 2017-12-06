from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .imageProcessingFunc.crystal_extractor import ProcessingFunction
from .utils import *

ps_func = ProcessingFunction()
temp_data_arr = []
temp_idx = 0


# for testing purpose only
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

            global temp_idx
            global temp_data_arr
            temp_idx = new_temp_data(temp_data_arr)
            temp = get_temp_data(temp_idx, temp_data_arr)

            temp.s_img_ori.img_data = cv2.imread(image_file_dir)
            temp.s_img_ori.func_name = 'upload'
            temp.s_img_cur = copy.copy(temp.s_img_ori)

            save_state(temp_idx, temp_data_arr)
            _, image_data = cv_to_json(temp.s_img_ori)
            return render(request, 'imageProcessing/processing_page.html', {'image_data':image_data, 'temp_index':temp_idx})
    else:
        form = DocumentForm()
    return render(request, 'imageProcessing/model_form_upload.html', {'form': form})


@csrf_exempt
def laplacian(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_idx, temp_data_arr)

    img_data = ps_func.laplacian_func(temp.s_img_cur.img_data)
    temp.update_s_img_cur('laplacian', img_data)
    #json_data, _ = cv_to_json(s_img_cur)
    save_state(temp_idx, temp_data_arr)
    json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def kmeans(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_idx, temp_data_arr)
    reset_current_image('kmeans', temp_idx, temp_data_arr)

    if request.method == 'POST':
        input = request.POST.get('input')
        print('input', input)
        input = int(input)

        img_data, temp.s_labels, gray_levels = ps_func.kmeans(temp.s_img_cur.img_data, segments=input)
        temp.update_s_img_cur('kmeans', img_data)
        #json_data, _ = cv_to_json(s_img_cur)
        save_state(temp_idx, temp_data_arr)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        #add gray levels of all extracted labels
        json_data['gray_levels']= gray_levels
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html',
                      {'image_data': image_data, 'temp_index': temp_idx})

@csrf_exempt
def lower_thresholding(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_idx, temp_data_arr)
    reset_current_image('lower_thesholding', temp_idx, temp_data_arr)

    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)

        img_data = ps_func.lower_thesholding(temp.s_img_ori.img_data, temp.s_img_cur.img_data, thresh_val=input)
        temp.update_s_img_cur('lower thresholding', img_data)

        save_state(temp_idx, temp_data_arr)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html',
                      {'image_data': image_data, 'temp_index': temp_idx})

@csrf_exempt
def upper_thresholding(request, temp_idx=0):

    global temp_data_arr
    reset_current_image('upper_theshoding', temp_idx, temp_data_arr)
    temp = get_temp_data(temp_idx, temp_data_arr)
    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)

        img_data= ps_func.upper_thesholding(temp.s_img_ori.img_data, temp.s_img_cur.img_data, thresh_val=input)
        temp.update_s_img_cur('upper thresholding', img_data)
        #json_data, _ = cv_to_json(s_img_cur)
        save_state(temp_idx, temp_data_arr)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': temp_idx})

@csrf_exempt
def undo_last_step(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_idx, temp_data_arr)

    if temp.s_undo_depth>=1:
        temp.s_undo_depth -=1
    temp.s_img_cur = copy.copy(temp.s_img_last_arr[temp.s_undo_depth])
    print('undo depth', temp.s_undo_depth)
    # json_data, _ = cv_to_json(s_img_cur)
    #save_state()
    json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def extract_crystal_mask(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_idx, temp_data_arr)
    reset_current_image('extract_crystal_mask', temp_idx, temp_data_arr)

    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)
        print ("crystal mask: ", input)

        img_data= ps_func.extract_crystal_mask(temp.s_img_cur.img_data, labels=temp.s_labels, user_chosen_label=input)
        temp.update_s_img_cur('extract crystal mask', img_data)
        #json_data, _ = cv_to_json(s_img_cur)
        save_state(temp_idx, temp_data_arr)

        temp.s_mask_cur = copy.copy(temp.s_img_cur)

        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html',
                      {'image_data': image_data, 'temp_index': temp_idx})

@csrf_exempt
def show_all_crystal(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_idx, temp_data_arr)

    img_data= ps_func.show_all_crystal(temp.s_img_ori.img_data, temp.s_img_cur.img_data)
    temp.update_s_img_cur('show all crystals', img_data)
    #json_data, _ = cv_to_json(s_img_cur)
    save_state(temp_idx, temp_data_arr)

    json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def show_top_area_crystal(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_idx, temp_data_arr)

    num_of_crystals = int(request.POST.get('input'))

    img_data = ps_func.show_top_area_crystals(temp.s_img_ori.img_data,
                                                              image_mask=temp.s_img_cur.img_data, num_of_crystals=num_of_crystals)
    temp.update_s_img_cur('top area crystals', img_data)
    save_state(temp_idx, temp_data_arr)
    json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    # json_data, _ = cv_to_json(s_img_cur)
    return JsonResponse(json_data)

@csrf_exempt
def reset(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_idx, temp_data_arr)

    temp.s_thumb_hist_arr = []
    temp.s_img_last_arr = []
    temp.s_undo_depth = 0
    temp.s_img_cur = copy.copy(temp.s_img_ori)

    save_state(temp_idx, temp_data_arr)

    json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    return JsonResponse(json_data)

@csrf_exempt
def set_image_from_thumbnail(request, temp_idx=0):
    global temp_data_arr
    temp = get_temp_data(temp_idx, temp_data_arr)

    if request.method == 'POST':
        input = request.POST.get('input')
        thumbnail_id = str(input)
        id = int(thumbnail_id.split("_")[1])

        temp.s_img_cur = temp.s_img_last_arr[id]
        temp.s_undo_depth = input
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html',
                      {'image_data': image_data, 'temp_index': temp_idx})

@csrf_exempt
def plot_histogram(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_idx, temp_data_arr)

    hist_y_axis, hist_x_axis = ps_func.plot_histogram(temp.s_img_cur.img_data, temp.s_mask_cur.img_data)
    json_data = {'x': hist_x_axis.tolist(), 'y': hist_y_axis.tolist()}
    return JsonResponse(json_data)

@csrf_exempt
def do_opening(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_idx, temp_data_arr)

    reset_current_image('do_opening', temp_idx, temp_data_arr)
    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        img_data= ps_func.opening(temp.s_img_cur.img_data, kernel_size, num_of_iter)
        temp.update_s_img_cur('opening', img_data)
        temp.s_mask_cur = copy.copy(temp.s_img_cur)

        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': temp_idx})


@csrf_exempt
def do_closing(request, temp_idx=0):


    global temp_data_arr
    temp = get_temp_data(temp_idx, temp_data_arr)

    reset_current_image('do_closing', temp_idx,temp_data_arr)

    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        img_data = ps_func.closing(temp.s_img_cur.img_data, kernel_size, num_of_iter)
        temp.update_s_img_cur('closing', img_data)
        temp.s_mask_cur = copy.copy(temp.s_img_cur)

        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': temp_idx})



@csrf_exempt
def do_erosion(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_idx, temp_data_arr)
    reset_current_image('do_erosion', temp_idx, temp_data_arr)

    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        img_data = ps_func.erosion(temp.s_img_cur.img_data, kernel_size, num_of_iter)
        temp.update_s_img_cur('erosion', img_data)
        temp.s_mask_cur = copy.copy(temp.s_img_cur)

        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': temp_idx})


@csrf_exempt
def do_dilation(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_idx, temp_data_arr)
    reset_current_image('do_dilation', temp_idx, temp_data_arr)

    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        img_data = ps_func.dilation(temp.s_img_cur.img_data, kernel_size, num_of_iter)
        temp.update_s_img_cur('dilation', img_data)
        temp.s_mask_cur = copy.copy(temp.s_img_cur)

        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': temp_idx})

@csrf_exempt
def update_mask(request, temp_idx=0):
    if request.method == 'POST':
        rgb_mask_data = request.POST.get('mask')
        rgb_mask = json_to_cv(rgb_mask_data)


        global temp_data_arr
        temp = get_temp_data(temp_idx, temp_data_arr)

        img_data, mask_data = ps_func.handle_mask(rgb_mask, temp.s_mask_cur.img_data, temp.s_img_ori.img_data)

        temp.update_s_img_cur('update mask', img_data)
        temp.s_mask_cur.img_data = mask_data
        temp.s_mask_cur.func_name = 'update mask'
        # s_img_cur = ps_func.show_all_crystal(s_img_ori=s_img_ori,
        #                                                     image_mask=s_mask_cur)
        # json_data, _ = cv_to_json(s_img_cur)
        save_state(temp_idx, temp_data_arr)

        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
        # json_data = thumbnail_plus_img_json(mask, s_thumb_hist_arr)
        # return JsonResponse(json_data, safe=False)

