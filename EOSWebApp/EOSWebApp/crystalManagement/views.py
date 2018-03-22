import zipfile
import cv2
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt

from EOSWebApp.crystalManagement.models import Crystal
from EOSWebApp.crystalManagement.utils import get_image_mask, HistProcessing
from EOSWebApp.imageProcessing.processingFunc.crystal_extractor import ProcessingFunction
from EOSWebApp.imageProcessing.models import UploadedImage, CrystalMask

from EOSWebApp.utils import IMAGE_URL, TEMP_DIR, timing, cv_to_json, absolute_file_dir

ps_func = ProcessingFunction()
hist_objs = []

@csrf_exempt
def library_page(request):
    if not request.user.is_authenticated():
        return render(request, 'user/login.html')
    else:
        images = UploadedImage.objects.filter(user=request.user)
        # update session info
        request.session['user_id'] = request.user.id
        # print(images)
        return render(request, 'crystalManagement/library.html', {'user': request.user, 'images': images})

# TODO: delete images, thumbnails, masks

#TODO: use compressed image
@csrf_exempt
def crystal_processing_page(request, mask_id):
    if not request.user.is_authenticated():
        return render(request, 'user/login.html')
    else:
        _, image_cv, mask_cv = get_image_mask(mask_id)
        _, ori_img_data = cv_to_json(image_cv, False)

        crystal_cv = ps_func.show_all_crystal(image_cv, mask_cv)
        _, crys_img_data = cv_to_json(crystal_cv, False)

        global hist_objs
        hist_objs = HistProcessing.generate_sim_table(mask_id, 80, 90)

        return render_to_response('crystalManagement/crystal_processing.html',
                      {'ori_img_data': ori_img_data, 'crys_img_data': crys_img_data, 'mask_id': int(mask_id),
                       'hist_objs': hist_objs   })

# Compare
@csrf_exempt
def plot_histogram(request, mask_id=0):
    _, image_cv, mask_cv = get_image_mask(mask_id)
    hist_y_axis, hist_x_axis = ps_func.plot_histogram(image_cv, mask_cv)
    json_data = {'x': hist_x_axis.tolist(), 'y': hist_y_axis.tolist()}
    return JsonResponse(json_data)

@csrf_exempt
def download_crystal(request, mask_id=0):
    #TODO: try except, clear temp dir, save zip to media

    mask, image_cv, mask_cv = get_image_mask(mask_id)
    # crystal_cv = ps_func.show_all_crystal(image_cv, mask_cv)
    file_infos,_ = ps_func.save_crystals_to_file(mask.name, TEMP_DIR, image_cv, mask_cv)
    #TODO: seperate to download and create crystal

    #TODO: choose correct dir to zip
    zf = zipfile.ZipFile('/home/long/EOSImages.zip', "w")
    for (file_dir, file_name) in file_infos:
        zf.write(file_dir, file_name)
    zf.close()

    zip_file = open('/home/long/EOSImages.zip', 'rb')
    response = HttpResponse(zip_file, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % 'EOSImages.zip'
    return response

@csrf_exempt
def delete_mask(request, mask_id):
    mask_id = int(mask_id)
    mask = CrystalMask.objects.get(pk=mask_id)
    mask.delete()

    images = UploadedImage.objects.filter(user=request.user)

    return render(request, 'crystalManagement/library.html', {'user': request.user, 'images': images})


@csrf_exempt
def modal_show_crystal(request, mask_id=0):
    #TODO: try except
    mask, image_cv, mask_cv = get_image_mask(mask_id)
    crystal_cv = ps_func.show_all_crystal(image_cv, mask_cv)
    _, image_data = cv_to_json(crystal_cv,False)

    return JsonResponse({'image_data': image_data, 'image_name': mask.name})


@csrf_exempt
@timing
def modal_show_individual_crystal(request, crystal_id):
    crystal_id = int(crystal_id)
    crystal = Crystal.objects.get(pk=crystal_id)
    # crystal_cv = cv2.imread(crystal.dir)
    crystal_cv = read_img(crystal.dir)
    _, image_data = cv_to_json(crystal_cv, False)

    return JsonResponse({'image_data': image_data, 'image_name': crystal.name})

@timing
def read_img(dir):
    return cv2.imread(dir)

@csrf_exempt
def modal_show_conf_graph(request, i):
    i = int(i)
    global hist_obj
    hist_obj = hist_objs[i]

    labels = []
    similarities = []
    for j in range (0, len(hist_obj.similarities)):
        if j is not i:
            label = hist_objs[j].crystal.name
            labels.append(label)
            similarity = hist_obj.similarities[j]['similarity_percentage']
            similarities.append(similarity)

    json_data = {'labels': labels, 'similarities': similarities}
    return JsonResponse(json_data)


