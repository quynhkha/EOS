from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from EOSWebApp.imageProcessing.services import *
from EOSWebApp.uploadImage.forms import *
from EOSWebApp.utils import shared_data, cv_to_json, get_func_name
from .processingFunc.crystal_extractor import ProcessingFunction
from .utils import *

ps_func = ProcessingFunction()
temp_data_arr = shared_data.temp_data_arr

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
def processing_page(request, image_id):
    # update the session info
    request.session['image_id'] = image_id
    print(request.session['image_id']) #debug

    global temp_data_arr
    state_data = new_state_data(temp_data_arr, request.session['image_id'])

    temp_image = TempImage()
    temp_mask = TempMask()
    temp_mask.save()
    temp_image.save(get_func_name() + state_data.get_ori_image().image.name.split('/')[-1], state_data.get_ori_image_cv(), get_func_name(), temp_mask)
    state_data.s_img_cur_id = temp_image.id

    # json_data, _ = cv_to_json(s_img_cur)
    state_data.save_state()

    # image = UploadedImage.objects.get(pk=request.session['image_id'])

    _, image_data = cv_to_json(state_data.get_cur_image_cv())
    # json_data = thumbnail_plus_img_json(state_data.s_img_cur, state_data.s_thumb_hist_arr)
    # return JsonResponse(json_data, safe=False)

    return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data, 'temp_index':0})
    #  TODO: fix with thumbnail


@csrf_exempt
def laplacian(request):
    json_data = s_laplacian(request)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def kmeans(request):
    json_data = s_kmeans(request)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def extract_crystal_mask(request):
    json_data = s_extract_crystal_mask(request)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def lower_thresholding_white(request):
    json_data = s_lower_thresholding_white(request)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def upper_thresholding_white(request):
    json_data = s_upper_thresholding_white(request)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def lower_thresholding_black(request):
    json_data = s_lower_thresholding_black(request)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def upper_thresholding_black(request):
    json_data = s_upper_thresholding_black(request)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def undo(request):

    json_data = s_undo(request)

    return JsonResponse(json_data, safe=False)

@csrf_exempt
def reset(request):

    json_data = s_reset(request)
    return JsonResponse(json_data)


@csrf_exempt
def show_all_crystal(request):

    json_data = s_show_all_crystal(request)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def fill_holes(request):
    json_data = s_fill_holes(request)
    return JsonResponse(json_data, safe=False)

# @csrf_exempt
# def do_fourier(request, temp_idx=0):
#     global temp_data_arr
#     state_data =get_state_data(temp_data_arr, request.session['image_id'])
#     img_data = ps_func.fourier(temp.s_img_cur.img_data)
#     temp.update_s_img_cur('fourier', img_data)
#     save_state(temp)
#
#     json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
#     return JsonResponse(json_data, safe=False)
#
# @csrf_exempt
# def do_backproj(request, temp_idx=0):
#     global temp_data_arr
#     state_data =get_state_data(temp_data_arr, request.session['image_id'])
#     img_data = ps_func.back_projection(temp.s_img_cur.img_data, temp.s_img_cur.img_data)
#     temp.update_s_img_cur('back-projection', img_data)
#     save_state(temp)
#
#     json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
#     return JsonResponse(json_data, safe=False)
#
@csrf_exempt
def show_top_area_crystal(request):
    json_data = s_show_top_area_crystal(request)
    return JsonResponse(json_data)


@csrf_exempt
def set_image_from_thumbnail(request):
    json_data = s_set_image_from_thumbnail(request)
    return JsonResponse(json_data, safe=False)



@csrf_exempt
def do_opening(request):
    json_data = s_do_opening(request)
    return JsonResponse(json_data, safe=False)



@csrf_exempt
def do_closing(request):
    json_data = s_do_closing(request)
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def do_erosion(request):
    json_data = s_do_erosion(request)
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def do_dilation(request):
    json_data = s_do_dilation(request)
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def do_morphgrad(request):
    json_data = s_do_morphgrad(request)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def do_tophat(request):
    json_data = s_do_tophat(request)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def do_blackhat(request):
    json_data = s_do_blackhat(request)
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def update_mask(request):
    # if request.method == 'POST':
    #     rgb_mask_data = request.POST.get('mask')
    #     rgb_mask = json_to_cv(rgb_mask_data)
    #
    #
    #     global temp_data_arstate_datatemp =get_state_data(temp_data_arr, request.session['image_id'])
    #
    #     img_data, mask_data = ps_func.handle_mask(rgb_mask, temp.s_mask_cur.img_data, temp.s_img_ori.img_data)
    #
    #     temp.update_s_img_cur('update mask', img_data)
    #     temp.s_mask_cur.img_data = mask_data
    #     temp.s_mask_cur.func_name = 'update mask'
    #     # s_img_cur = ps_func.show_all_crystal(s_img_ori=s_img_ori,
    #     #                                                     image_mask=s_mask_cur)
    #     # json_data, _ = cv_to_json(s_img_cur)
    #
    #     save_state(temp)
    #
    #     json_data = thumbnail_plus_img_json(temp.s_img_cur, temp.s_thumb_hist_arr)
    #     return JsonResponse(json_data, safe=False)
    #     # json_data = thumbnail_plus_img_json(mask, s_thumb_hist_arr)
    #     # return JsonResponse(json_data, safe=False)

    json_data = s_update_mask(request)
    return JsonResponse(json_data, safe=False)

@csrf_exempt
def noise_removal(request):
    json_data = s_noise_removal(request)
    return JsonResponse(json_data, safe=False)


@csrf_exempt
def save_processed(request):
    # TODO: check whether is a mask
    json_data = s_save_processed(request)
    return JsonResponse(json_data, safe=False)
    # return JsonResponse({'mask_dir': mask_dir}, safe=False)


@csrf_exempt
def delete_image(request, image_id):
    image_id = int(image_id)
    image = UploadedImage.objects.get(pk=image_id)
    image.delete()
    images = UploadedImage.objects.filter(user=request.user)
    return render(request, 'index.html', {'user': request.user, 'images': images})

@csrf_exempt
def large_thumbnail(request, thumbnail_id):
    json_data = s_large_thumbnail(request, thumbnail_id)

    return JsonResponse(json_data)

