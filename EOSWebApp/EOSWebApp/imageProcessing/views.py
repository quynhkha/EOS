import zipfile

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from EOSWebApp.crystalManagement.models import Crystal
from EOSWebApp.utils import shared_data, THUMBNAIL_URL, IMAGE_URL, CRYSTAL_MASK_URL, CRYSTAL_URL
from .forms import *
from .processingFunc.crystal_extractor import ProcessingFunction
from .utils import *

ps_func = ProcessingFunction()
temp_data_arr = shared_data.temp_data_arr
temp_idx = 0

# FIXME: deprecated
# for testing purpose only
def show_base64(request):
    opencv_img = cv2.imread('/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.small.png')
    json_data, _= cv_to_json(opencv_img)
    return JsonResponse(json_data, safe=False)


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'user/login.html')
    else:
        images = UploadedImage.objects.filter(user=request.user)
        # update session info
        request.session['user_id'] = request.user.id
        # print(images)
        return render(request, 'index.html', {'user': request.user, 'images': images})

@csrf_exempt
@login_required
def upload_image(request):
    if request.method == 'POST':
        imageForm = ImageForm(request.POST, request.FILES)
        if imageForm.is_valid():
            imageDB = imageForm.save()

            file= request.FILES['document']
            print("filename", file.name, "file content type", file.content_type, "file size", file.size)
            imageDB.filename = file.name
            imageDB.user = request.user
            imageDB.save()


            image_file_dir = absolute_file_dir(file.name, IMAGE_URL)
            print ("image file dir", image_file_dir)
            thumbnail_data = compress_image(cv2.imread(image_file_dir))

            thumbnail_name = file.name + "_thumbnail.png"
            cv2.imwrite(absolute_file_dir(thumbnail_name, THUMBNAIL_URL), thumbnail_data)
            imageDB.thumbnail_url = THUMBNAIL_URL + thumbnail_name
            imageDB.save()

            return redirect('imageProcessing:processing_page', image_id=imageDB.id)
            #return render(request, 'imageProcessing/processing_page.html', {'image_data':image_data, 'temp_index':temp_idx})
    else:
        imageForm =ImageForm()
    return render(request, 'imageProcessing/upload_image.html', {'form': imageForm})

@csrf_exempt
def processing_page(request, image_id):
    # update the session info
    request.session['image_id'] = image_id
    print(request.session['image_id']) #debug

    global temp_data_arr
    temp = new_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])

    image = UploadedImage.objects.get(pk=request.session['image_id'])
    image_file_dir = absolute_file_dir(image.filename, IMAGE_URL)
    temp.s_img_ori.img_data = cv2.imread(image_file_dir)
    temp.s_img_ori.func_name = 'upload'
    temp.s_img_cur = copy.copy(temp.s_img_ori)

    # save_state(temp)

    # temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    _, image_data = cv_to_json(temp.s_img_ori)
    json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    # return JsonResponse(json_data, safe=False)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index':0})


@csrf_exempt
def laplacian(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])

    img_data = ps_func.laplacian_func(temp.s_img_cur.img_data)
    temp.update_s_img_cur('laplacian', img_data)
    #json_data, _ = cv_to_json(s_img_cur)
    save_state(temp)
    json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def kmeans(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    #reset_current_image('kmeans', temp_idx, temp_data_arr)

    if request.method == 'POST':
        input = request.POST.get('input')
        print('input', input)
        input = int(input)

        img_data, temp.s_labels, gray_levels = ps_func.kmeans(temp.s_img_cur.img_data, segments=input)
        temp.update_s_img_cur('kmeans', img_data, gray_levels)
        #json_data, _ = cv_to_json(s_img_cur)
        save_state(temp)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        #add gray levels of all extracted labels
        # json_data['gray_levels']= gray_levels

        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html',
                  {'image_data': image_data, 'temp_index': temp_idx})

@csrf_exempt
def lower_thresholding_white(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    #reset_current_image('lower_thesholding', temp_idx, temp_data_arr)

    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)

        img_data = ps_func.lower_thesholding_white(temp.s_img_ori.img_data, temp.s_img_cur.img_data, thresh_val=input)
        temp.update_s_img_cur('lower thresholding white', img_data)

        save_state(temp)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html',
                  {'image_data': image_data, 'temp_index': temp_idx})

@csrf_exempt
def upper_thresholding_white(request, temp_idx=0):

    global temp_data_arr
    #reset_current_image('upper_theshoding', temp_idx, temp_data_arr)
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)

        img_data= ps_func.upper_thesholding_white(temp.s_img_ori.img_data, temp.s_img_cur.img_data, thresh_val=input)
        temp.update_s_img_cur('upper thresholding white', img_data)
        #json_data, _ = cv_to_json(s_img_cur)
        save_state(temp)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': temp_idx})

@csrf_exempt
def lower_thresholding_black(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    #reset_current_image('lower_thesholding', temp_idx, temp_data_arr)

    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)

        img_data = ps_func.lower_thesholding_black(temp.s_img_ori.img_data, temp.s_img_cur.img_data, thresh_val=input)
        temp.update_s_img_cur('lower thresholding black', img_data)

        save_state(temp)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html',
                  {'image_data': image_data, 'temp_index': temp_idx})

@csrf_exempt
def upper_thresholding_black(request, temp_idx=0):

    global temp_data_arr
    #reset_current_image('upper_theshoding', temp_idx, temp_data_arr)
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)

        img_data= ps_func.upper_thesholding_black(temp.s_img_ori.img_data, temp.s_img_cur.img_data, thresh_val=input)
        temp.update_s_img_cur('upper thresholding black', img_data)
        #json_data, _ = cv_to_json(s_img_cur)
        save_state(temp)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': temp_idx})

@csrf_exempt
def undo_last_step(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])

    if temp.s_undo_depth>=1:
        temp.s_undo_depth -=1
    temp.s_img_cur = copy.copy(temp.s_img_last_arr[temp.s_undo_depth])
    print('undo depth', temp.s_undo_depth)
    # json_data, _ = cv_to_json(s_img_cur)
    # save_state(temp)
    json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def extract_crystal_mask(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
        # reset_current_image('extract_crystal_mask', temp_idx, temp_data_arr)

    if request.method == 'POST':
        input = request.POST.get('input')
        input = int(input)
        print ("crystal mask: ", input)

        img_data= ps_func.extract_crystal_mask(temp.s_img_cur.img_data, labels=temp.s_labels, user_chosen_label=input)
        temp.update_s_img_cur('extract crystal mask', img_data)

        #json_data, _ = cv_to_json(s_img_cur)
        save_state(temp)

        temp.s_mask_cur = copy.copy(temp.s_img_cur)
        temp.s_mask_cur.func_name = 'extract crystal mask'
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html',
                  {'image_data': image_data, 'temp_index': temp_idx})

@csrf_exempt
def show_all_crystal(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])

    img_data= ps_func.show_all_crystal(temp.s_img_ori.img_data, temp.s_mask_cur.img_data)
    temp.update_s_img_cur('show all crystals', img_data)

    #json_data, _ = cv_to_json(s_img_cur)
    save_state(temp)

    json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def fill_holes(request, temp_idx=0):
    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    #
    # lo = int(request.POST.get('lo'))
    # hi = int(request.POST.get('lo'))
    # conn = int(request.POST.get('conn'))
    # fixed_range = int(request.POST.get('fixed_range'))
    #
    # print('lo, hi, conn, fixed range', lo, hi, conn, fixed_range)
    # flags = conn
    # if fixed_range:
    #     flags |= cv2.FLOODFILL_FIXED_RANGE
    #
    # mask_data, _= ps_func.fill_holes(temp.s_img_ori.img_data, temp.s_mask_cur.img_data, lo, hi, flags)

    # mask_data, _ = ps_func.fill_holes(temp.s_img_ori.img_data, temp.s_mask_cur.img_data)
    mask_data, filled_image = ps_func.imfill(temp.s_img_ori.img_data, temp.s_img_cur.img_data)
    temp.update_s_img_cur('fill holes', mask_data)
    temp.s_mask_cur.img_data = mask_data
    temp.s_mask_cur.func_name = 'fill holes'

    # json_data, _ = cv_to_json(s_img_cur)
    save_state(temp)

    json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def do_fourier(request, temp_idx=0):
    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    img_data = ps_func.fourier(temp.s_img_cur.img_data)
    temp.update_s_img_cur('fourier', img_data)
    save_state(temp)

    json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def do_backproj(request, temp_idx=0):
    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    img_data = ps_func.back_projection(temp.s_img_cur.img_data, temp.s_img_cur.img_data)
    temp.update_s_img_cur('back-projection', img_data)
    save_state(temp)

    json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def show_top_area_crystal(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])

    num_of_crystals = int(request.POST.get('input'))

    img_data, mask = ps_func.show_top_area_crystals(temp.s_img_ori.img_data,
                                                              image_mask=temp.s_mask_cur.img_data, num_of_crystals=num_of_crystals)
    temp.update_s_img_cur('top area crystals', img_data)
    temp.s_mask_cur.img_data = mask
    temp.s_mask_cur.func_name = 'top area crystals'
    save_state(temp)
    json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    # json_data, _ = cv_to_json(s_img_cur)
    return JsonResponse(json_data)

@csrf_exempt
def reset(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])

    temp.s_thumb_hist_arr = []
    temp.s_img_last_arr = []
    temp.s_undo_depth = 0
    temp.s_img_cur = copy.copy(temp.s_img_ori)

    save_state(temp)

    json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    return JsonResponse(json_data)

@csrf_exempt
def set_image_from_thumbnail(request, temp_idx=0):
    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])

    if request.method == 'POST':
        input = request.POST.get('input')
        thumbnail_id = str(input)
        id = int(thumbnail_id.split("_")[1])

        temp.s_img_cur = temp.s_img_last_arr[id]
        temp.s_undo_depth = id
        temp.s_just_recovered = True
        print("Extract img number", input)

        save_state(temp)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)

        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html',
                  {'image_data': image_data, 'temp_index': temp_idx})


@csrf_exempt
def do_opening(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])

    #reset_current_image('do_opening', temp_idx, temp_data_arr)
    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        img_data= ps_func.opening(temp.s_img_cur.img_data, kernel_size, num_of_iter)
        temp.update_s_img_cur('opening', img_data)
        temp.s_mask_cur = copy.copy(temp.s_img_cur)

        save_state(temp)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': temp_idx})


@csrf_exempt
def do_closing(request, temp_idx=0):


    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])

    #reset_current_image('do_closing', temp_idx,temp_data_arr)

    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        img_data = ps_func.closing(temp.s_img_cur.img_data, kernel_size, num_of_iter)
        temp.update_s_img_cur('closing', img_data)
        temp.s_mask_cur = copy.copy(temp.s_img_cur)

        save_state(temp)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': temp_idx})



@csrf_exempt
def do_erosion(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    #reset_current_image('do_erosion', temp_idx, temp_data_arr)

    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        img_data = ps_func.erosion(temp.s_img_cur.img_data, kernel_size, num_of_iter)
        temp.update_s_img_cur('erosion', img_data)
        temp.s_mask_cur = copy.copy(temp.s_img_cur)

        save_state(temp)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': temp_idx})


@csrf_exempt
def do_dilation(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    #reset_current_image('do_dilation', temp_idx, temp_data_arr)

    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        img_data = ps_func.dilation(temp.s_img_cur.img_data, kernel_size, num_of_iter)
        temp.update_s_img_cur('dilation', img_data)
        temp.s_mask_cur = copy.copy(temp.s_img_cur)

        save_state(temp)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': temp_idx})



@csrf_exempt
def do_morphgrad(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    #reset_current_image('do_dilation', temp_idx, temp_data_arr)

    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        img_data = ps_func.morph_gradient(temp.s_img_cur.img_data, kernel_size, num_of_iter)
        temp.update_s_img_cur('morph-gradient', img_data)
        temp.s_mask_cur = copy.copy(temp.s_img_cur)

        save_state(temp)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': temp_idx})



@csrf_exempt
def do_tophat(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    #reset_current_image('do_dilation', temp_idx, temp_data_arr)

    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        img_data = ps_func.top_hat(temp.s_img_cur.img_data, kernel_size, num_of_iter)
        temp.update_s_img_cur('tophat', img_data)
        temp.s_mask_cur = copy.copy(temp.s_img_cur)

        save_state(temp)
        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
    else:
        _, image_data = cv_to_json(temp.s_img_cur)
    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index': temp_idx})




@csrf_exempt
def do_blackhat(request, temp_idx=0):

    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    #reset_current_image('do_dilation', temp_idx, temp_data_arr)

    if request.method == 'POST':
        kernel_size = int(request.POST.get('kernel_size'))
        num_of_iter = int(request.POST.get('num_of_iter'))

        img_data = ps_func.black_hat(temp.s_img_cur.img_data, kernel_size, num_of_iter)
        temp.update_s_img_cur('blackhat', img_data)
        temp.s_mask_cur = copy.copy(temp.s_img_cur)

        save_state(temp)
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
        temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])

        img_data, mask_data = ps_func.handle_mask(rgb_mask, temp.s_mask_cur.img_data, temp.s_img_ori.img_data)

        temp.update_s_img_cur('update mask', img_data)
        temp.s_mask_cur.img_data = mask_data
        temp.s_mask_cur.func_name = 'update mask'
        # s_img_cur = ps_func.show_all_crystal(s_img_ori=s_img_ori,
        #                                                     image_mask=s_mask_cur)
        # json_data, _ = cv_to_json(s_img_cur)

        save_state(temp)

        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)
        # json_data = thumbnail_plus_img_json(mask, s_thumb_hist_arr)
        # return JsonResponse(json_data, safe=False)

@csrf_exempt
def noise_removal(request, temp_idx=0):
    if request.method == 'POST':
        area_thresh = request.POST.get('input')
        area_thresh = int(area_thresh)

        global temp_data_arr
        temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])

        img_data = ps_func.noise_removal(temp.s_mask_cur.img_data, area_thresh)
        temp.update_s_img_cur('noise removal', img_data)
        temp.s_mask_cur.img_data = img_data
        temp.s_mask_cur.func_name = 'noise removal'

        save_state(temp)

        json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
        return JsonResponse(json_data, safe=False)


@csrf_exempt
def save_processed(request, temp_idx=0):
    # TODO: check whether is a mask

    crystal_name = str(request.POST.get('name'))
    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])

    image = UploadedImage.objects.get(pk=request.session['image_id'])
    # original image name (extract name from path, ex: document/imageName)+ current time
    _, image_name = image.document.name.split('/', 1)
    mask_dir= absolute_file_dir(image_name, CRYSTAL_MASK_URL) + str(int(time.time())) + "_mask.png"
    print(mask_dir)
    cv2.imwrite(mask_dir, temp.s_mask_cur.img_data)
    mask = CrystalMask.objects.create(name= crystal_name, image = image, mask_dir = mask_dir)
    mask.save()

    # save crystal to files
    CRYSTAL_DIR = PROJECT_ROOT +CRYSTAL_URL

    file_infos = ps_func.save_crystals_to_file(crystal_name, CRYSTAL_DIR, temp.s_img_ori.img_data, temp.s_mask_cur.img_data)
    for (file_dir, file_name) in file_infos:
        crystal = Crystal.objects.create(mask=mask, name=file_name, dir=file_dir)
        crystal.save()

    return JsonResponse({'mask_dir': mask_dir}, safe=False)


@csrf_exempt
def delete_image(request, image_id):
    image_id = int(image_id)
    image = UploadedImage.objects.get(pk=image_id)

    # delete image from disk
    delete_file(image.document.path)
    # delete thumb from disk
    delete_file(str(BASE_DIR)+image.thumbnail_url)
    # delete from db
    image.delete()

    images = UploadedImage.objects.filter(user=request.user)

    return render(request, 'index.html', {'user': request.user, 'images': images})

@csrf_exempt
def large_thumbnail(request, thumbnail_id):
    # thumbnail_id = str(thumbnail_id)
    # id = thumbnail_id.split('_')[1]
    id = int(thumbnail_id)
    print(id)
    global temp_data_arr
    temp = get_temp_data(temp_data_arr, request.session['user_id'], request.session['image_id'])
    state_img = temp.s_img_last_arr[id]
    print(state_img)
    compressed_img = compress_image(state_img.img_data, mod_size=4)
    _, image_data = cv_to_json(compressed_img, False)

    return JsonResponse({'image_data': image_data})

