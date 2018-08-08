import time

from EOSWebApp.crystalManagement.models import Crystal
from EOSWebApp.imageProcessing.models import TempImage, UploadedImage, CrystalMask
from EOSWebApp.imageProcessing.processingFunc.crystal_extractor import ProcessingFunction
from EOSWebApp.imageProcessing.utils import get_state_data, update_state_data, get_thumbnail_plus_img_json
from EOSWebApp.utils import shared_data, get_func_name, compress_image, cv_to_json, absolute_file_dir, CRYSTAL_MASK_URL, \
    json_to_cv
import numpy as np
import pandas as pd 
from sklearn.cluster import KMeans
from django.core.files.base import File

ps_func = ProcessingFunction()
temp_data_arr = shared_data.temp_data_arr
CRYSTAL_DIR = '/home/long/EOS/'
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

    func_setting = request.POST.get('func_setting')
    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    image_cv, labels, gray_levels = ps_func.kmeans(state_data.get_cur_image_cv(), segments=input)
    #print ("labels: ", labels, "gray_levels: ", gray_levels)
    #print("******max of labels", np.amax(labels))
    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, mask_data=np.uint8(labels),
                      func_setting= func_setting, gray_levels=np.array(gray_levels).tolist(), update_mask=True)
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data

def s_extract_crystal_mask(request):
    input = request.POST.get('input')
    input = int(input)
    print("crystal mask: ", input)
    func_setting = request.POST.get('func_setting')

    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    # prev_temp_image_id = state_data.s_img_hist_ids[-2] #top always the original image

    # image_cv = ps_func.extract_crystal_mask(state_data.get_cur_image_cv(), labels=state_data.get_temp_mask_cv(prev_temp_image_id), user_chosen_label=input)
    image_cv = ps_func.extract_crystal_mask(state_data.get_cur_image_cv(),
                                            labels=state_data.get_temp_mask_cv(state_data.s_img_mask_id), user_chosen_label=input)
    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, mask_data=image_cv,
                      func_setting=func_setting, update_mask=True)
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data

def s_lower_thresholding_white(request):
    input = request.POST.get('input')
    input = int(input)
    func_setting = request.POST.get('func_setting')

    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    image_cv = ps_func.lower_thesholding_white(state_data.get_ori_image_cv(), state_data.get_cur_image_cv(), thresh_val=input)

    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, func_setting= func_setting)
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data

def s_upper_thresholding_white(request):
    input = request.POST.get('input')
    input = int(input)
    func_setting = request.POST.get('func_setting')

    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    image_cv = ps_func.upper_thesholding_white(state_data.get_ori_image_cv(), state_data.get_cur_image_cv(), thresh_val=input)

    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, func_setting= func_setting )
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data

def s_lower_thresholding_black(request):
    input = request.POST.get('input')
    input = int(input)
    func_setting = request.POST.get('func_setting')

    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    image_cv = ps_func.lower_thesholding_black(state_data.get_ori_image_cv(), state_data.get_cur_image_cv(), thresh_val=input)

    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, func_setting= func_setting)
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data

def s_upper_thresholding_black(request):
    input = request.POST.get('input')
    input = int(input)
    func_setting = request.POST.get('func_setting')

    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    image_cv = ps_func.upper_thesholding_black(state_data.get_ori_image_cv(), state_data.get_cur_image_cv(),thresh_val=input)

    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, func_setting= func_setting)
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data

def s_reverse_color(request):
    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    image_cv = ps_func.reverse_color_func(state_data.get_cur_image_cv())
    import pdb
    pdb.set_trace()
    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv)
    json_data = get_thumbnail_plus_img_json(state_data)
    return json_data

def s_undo(request):
    state_data = get_state_data(temp_data_arr, request.session['image_id'])

    if state_data.s_pointer >= 1:
        state_data.s_pointer -= 1
    state_data.s_img_cur_id = state_data.s_img_hist_ids[state_data.s_pointer]
    print('undo---pointer', state_data.s_pointer)
    # json_data, _ = cv_to_json(s_img_cur)
    # save_state(temp)
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data

def s_show_all_crystal(request):
    state_data =get_state_data(temp_data_arr, request.session['image_id'])

    image_cv= ps_func.show_all_crystal(state_data.get_ori_image_cv(), state_data.get_temp_mask_cv(state_data.s_img_mask_id))

    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv)
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data

#TODO: how to let user know theu need to pass a mask
def s_fill_holes(request):
    state_data = get_state_data(temp_data_arr, request.session['image_id'])

    mask_data, filled_image = ps_func.imfill(state_data.get_ori_image_cv(),state_data.get_temp_mask_cv(state_data.s_img_mask_id))
    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=mask_data, mask_data=mask_data, update_mask=True)

    json_data = get_thumbnail_plus_img_json(state_data)
    return json_data

def s_show_top_area_crystal(request):

    state_data = get_state_data(temp_data_arr, request.session['image_id'])

    num_of_crystals = int(request.POST.get('input'))
    func_setting = request.POST.get('func_setting')


    image_cv, mask_data = ps_func.show_top_area_crystals(state_data.get_ori_image_cv(),
                                                    image_mask=state_data.get_temp_mask_cv(state_data.s_img_mask_id),
                                                    num_of_crystals=num_of_crystals)
    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, mask_data=mask_data,
                      update_mask=True, func_setting= func_setting,)

    json_data = get_thumbnail_plus_img_json(state_data)
    return json_data

def s_set_image_from_thumbnail(request):

    state_data = get_state_data(temp_data_arr, request.session['image_id'])

    input = request.POST.get('input')

    thumbnail_id = str(input)
    id = int(thumbnail_id.split("_")[1])

    state_data.s_pointer = id
    state_data.s_img_cur_id = state_data.s_img_hist_ids[state_data.s_pointer]
    print('set_img_thumbnail---pointer', state_data.s_pointer)
    # json_data, _ = cv_to_json(s_img_cur)
    # save_state(temp)
    json_data = get_thumbnail_plus_img_json(state_data)

    return json_data

def s_large_thumbnail(request, thumbnail_id):
    id = int(thumbnail_id)
    print(id)

    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    temp_image_id = state_data.s_img_hist_ids[id]
    image_cv = state_data.get_temp_image_cv(temp_image_id)
    compressed_img = compress_image(image_cv, mod_size=4)
    _, image_data = cv_to_json(compressed_img, False)

    json_data = {'image_data': image_data}

    return json_data


def s_do_opening(request):
    state_data =get_state_data(temp_data_arr, request.session['image_id'])
    kernel_size = int(request.POST.get('kernel_size'))
    num_of_iter = int(request.POST.get('num_of_iter'))
    func_setting = request.POST.get('func_setting')

    image_cv= ps_func.opening(state_data.get_cur_image_cv(), kernel_size, num_of_iter)
    func_name = get_func_name()

    if len(image_cv.shape) ==2: # only update mask if user process mask with this func
        update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, mask_data=image_cv,
                          func_setting=func_setting, update_mask=True)

    else:
        update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, func_setting= func_setting)
    json_data = get_thumbnail_plus_img_json(state_data)
    return json_data

def s_do_closing(request):
    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    kernel_size = int(request.POST.get('kernel_size'))
    num_of_iter = int(request.POST.get('num_of_iter'))
    func_setting = request.POST.get('func_setting')

    image_cv= ps_func.closing(state_data.get_cur_image_cv(), kernel_size, num_of_iter)
    func_name = get_func_name()

    if len(image_cv.shape) ==2: # only update mask if user process mask with this func
        update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, mask_data=image_cv,
                          func_setting=func_setting, update_mask=True)

    else:
        update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, func_setting= func_setting)
    json_data = get_thumbnail_plus_img_json(state_data)
    return json_data


def s_do_erosion(request):
    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    kernel_size = int(request.POST.get('kernel_size'))
    num_of_iter = int(request.POST.get('num_of_iter'))
    func_setting = request.POST.get('func_setting')

    image_cv = ps_func.erosion(state_data.get_cur_image_cv(), kernel_size, num_of_iter)
    func_name = get_func_name()

    if len(image_cv.shape) == 2:  # only update mask if user process mask with this func
        update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, mask_data=image_cv,
                          func_setting=func_setting, update_mask=True)

    else:
        update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, func_setting= func_setting)
    json_data = get_thumbnail_plus_img_json(state_data)
    return json_data

def s_do_dilation(request):
    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    kernel_size = int(request.POST.get('kernel_size'))
    num_of_iter = int(request.POST.get('num_of_iter'))
    func_setting = request.POST.get('func_setting')

    image_cv = ps_func.dilation(state_data.get_cur_image_cv(), kernel_size, num_of_iter)
    func_name = get_func_name()

    if len(image_cv.shape) == 2:  # only update mask if user process mask with this func
        update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, mask_data=image_cv,
                          func_setting=func_setting, update_mask=True)

    else:
        update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, func_setting= func_setting)
    json_data = get_thumbnail_plus_img_json(state_data)
    return json_data

def s_save_processed(request):

    crystal_name = str(request.POST.get('name'))
    state_data =get_state_data(temp_data_arr, request.session['image_id'])

    #
    # image = UploadedImage.objects.get(pk=request.session['image_id'])
    # # original image name (extract name from path, ex: document/imageName)+ current time
    # _, image_name = image.document.name.split('/', 1)
    # mask_dir= absolute_file_dir(image_name, CRYSTAL_MASK_URL) + str(int(time.time())) + "_mask.png"
    # print(mask_dir)
    # cv2.imwrite(mask_dir, temp.s_mask_cur.img_data)
    # mask = CrystalMask.objects.create(name= crystal_name, image = image, mask_dir = mask_dir)
    # mask.save()
    img_height, img_width = state_data.get_ori_image_cv().shape[:2]
    image = state_data.get_ori_image()
    file_infos, crystal_datas, crystal_areas, crystal_height, crystal_width, crystal_mean, crystal_standard_deviation, centroids, labels, inertia = ps_func.save_crystals_to_file(crystal_name, CRYSTAL_DIR, state_data.get_ori_image_cv(),
                                                     state_data.get_temp_mask_cv(state_data.s_img_mask_id))

    df = pd.DataFrame(data=np.array(crystal_mean) / 255., columns=['Mean'])
    df['Standard Deviation'] = np.array(crystal_standard_deviation) / 255.
    df['Pixel Area'] = np.array(crystal_areas) / img_height / img_width 

    crystal_mask = CrystalMask()
    crystal_mask.save(image=image, csv_data=df, name=crystal_name, mask_data=state_data.get_temp_mask_cv(state_data.s_img_mask_id))


    # file_infos = ps_func.save_crystals_to_file(crystal_name, CRYSTAL_DIR, temp.s_img_ori.img_data, temp.s_mask_cur.img_data)
    # for (file_dir, file_name) in file_infos:
    #     crystal = Crystal.objects.create(mask=mask, name=file_name, dir=file_dir)
    #     crystal.save()
    
    
    for i, crystal_data in enumerate(crystal_datas):
        
        crystal = Crystal()

        # round to 2 decimal place
        pixel_area = round(float(crystal_areas[i]), 2)
        dist_per_pixel = image.dist_per_pixel
        real_area = round(pixel_area * dist_per_pixel * dist_per_pixel, 2)
        mean = crystal_mean[i]
        standard_deviation = crystal_standard_deviation[i]
        height = crystal_height[i]
        width = crystal_width[i]

        crystal.save(mask=crystal_mask, name=crystal_name+"_"+str(i), crystal_data=crystal_data,
                     pixel_area=pixel_area, real_area=real_area, mean=mean, standard_deviation=standard_deviation, 
                     height=height, width=width)

    json_data = {'mask_id': crystal_mask.id}
    return json_data

def s_do_blackhat(request):

    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    # reset_current_image('do_dilation', temp_idx, temp_data_arr)
    kernel_size = int(request.POST.get('kernel_size'))
    num_of_iter = int(request.POST.get('num_of_iter'))
    func_setting = request.POST.get('func_setting')

    image_cv = ps_func.black_hat(state_data.get_cur_image_cv(), kernel_size, num_of_iter)
    func_name = get_func_name()

    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, func_setting= func_setting)

    json_data = get_thumbnail_plus_img_json(state_data)
    return json_data


def s_do_morphgrad(request):
    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    kernel_size = int(request.POST.get('kernel_size'))
    num_of_iter = int(request.POST.get('num_of_iter'))
    func_setting = request.POST.get('func_setting')

    image_cv = ps_func.morph_gradient(state_data.get_cur_image_cv(), kernel_size, num_of_iter)
    func_name = get_func_name()

    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, func_setting= func_setting)

    json_data = get_thumbnail_plus_img_json(state_data)
    return json_data

def s_do_tophat(request):
    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    kernel_size = int(request.POST.get('kernel_size'))
    num_of_iter = int(request.POST.get('num_of_iter'))
    func_setting = request.POST.get('func_setting')

    image_cv = ps_func.top_hat(state_data.get_cur_image_cv(), kernel_size, num_of_iter)
    func_name = get_func_name()

    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, func_setting= func_setting)

    json_data = get_thumbnail_plus_img_json(state_data)
    return json_data

def s_noise_removal(request):
    state_data =get_state_data(temp_data_arr, request.session['image_id'])

    area_thresh = request.POST.get('input')
    area_thresh = int(area_thresh)
    func_setting = request.POST.get('func_setting')

    image_cv = ps_func.noise_removal(state_data.get_cur_image_cv(), area_thresh)

    func_name = get_func_name()

    if len(image_cv.shape) ==2: # only update mask if user process mask with this func
        update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, mask_data=image_cv,
                          update_mask=True, func_setting= func_setting)

    else:
        update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, func_setting= func_setting)
    json_data = get_thumbnail_plus_img_json(state_data)
    return json_data


def s_update_mask(request):
    rgb_mask_data = request.POST.get('mask')
    rgb_mask = json_to_cv(rgb_mask_data)

    state_data = get_state_data(temp_data_arr, request.session['image_id'])
    image_cv, mask_cv = ps_func.handle_mask(rgb_mask, state_data.get_temp_mask_cv(state_data.s_img_mask_id), state_data.get_ori_image_cv())


    func_name = get_func_name()
    update_state_data(state_data=state_data, func_name=func_name, image_cv=image_cv, mask_data=mask_cv, update_mask=True)
    json_data = get_thumbnail_plus_img_json(state_data)
    return json_data



