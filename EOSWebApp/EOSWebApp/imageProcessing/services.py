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
    print ("labels: ", labels, "gray_levels: ", gray_levels)
    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, gray_levels=np.array(gray_levels).tolist(), k_labels=np.array(labels).tolist())
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data