from EOSWebApp.imageProcessing.models import TempImage
from EOSWebApp.imageProcessing.processingFunc.crystal_extractor import ProcessingFunction
from EOSWebApp.imageProcessing.utils import get_state_data, update_state_data, get_thumbnail_plus_img_json
from EOSWebApp.utils import shared_data, get_func_name
import numpy as np

ps_func = ProcessingFunction()
temp_data_arr = shared_data.temp_data_arr

def s_laplacian(request):
    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    image_cv = ps_func.laplacian_func(state_data.get_cur_image_cv())
    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv)
    json_data = get_thumbnail_plus_img_json(state_data)
    return json_data

def s_kmeans(request):
    input = request.POST.get('input')
    print('kmean input', input)
    input = int(input)

    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    image_cv, labels, gray_levels = ps_func.kmeans(state_data.get_cur_image_cv(), segments=input)
    #print ("labels: ", labels, "gray_levels: ", gray_levels)
    #print("******max of labels", np.amax(labels))
    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, mask_data=np.uint8(labels), gray_levels=np.array(gray_levels).tolist())
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data

def s_extract_crystal_mask(request):
    input = request.POST.get('input')
    input = int(input)
    print("crystal mask: ", input)

    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    prev_temp_image_id = state_data.s_img_hist_ids[-2] #top always the original image

    image_cv = ps_func.extract_crystal_mask(state_data.get_cur_image_cv(), labels=state_data.get_temp_mask_cv(prev_temp_image_id), user_chosen_label=input)

    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv)
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data

def s_lower_thresholding_white(request):
    input = request.POST.get('input')
    input = int(input)

    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    image_cv = ps_func.lower_thesholding_white(state_data.get_ori_image_cv(), state_data.get_cur_image_cv(), thresh_val=input)

    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv)
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data

def s_upper_thresholding_white(request):
    input = request.POST.get('input')
    input = int(input)

    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    image_cv = ps_func.upper_thesholding_white(state_data.get_ori_image_cv(), state_data.get_cur_image_cv(), thresh_val=input)

    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv)
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data

def s_lower_thresholding_black(request):
    input = request.POST.get('input')
    input = int(input)

    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    image_cv = ps_func.lower_thesholding_black(state_data.get_ori_image_cv(), state_data.get_cur_image_cv(), thresh_val=input)

    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv)
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data

def s_upper_thresholding_black(request):
    input = request.POST.get('input')
    input = int(input)

    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    image_cv = ps_func.upper_thesholding_black(state_data.get_ori_image_cv(), state_data.get_cur_image_cv(), thresh_val=input)

    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv)
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data
