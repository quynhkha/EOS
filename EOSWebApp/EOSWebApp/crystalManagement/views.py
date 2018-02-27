import zipfile
import cv2
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from EOSWebApp.imageProcessing.processingFunc.crystal_extractor import ProcessingFunction
from EOSWebApp.imageProcessing.models import UploadedImage, CrystalMask
from EOSWebApp.imageProcessing.utils import absolute_file_dir, StateImage, cv_to_json, get_temp_data
from EOSWebApp.utils import IMAGE_URL

ps_func = ProcessingFunction()

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
    file_infos = ps_func.save_crystals_to_file(mask.name, '/home/long/EOSImages/', image_cv, mask_cv)

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
    mask_id = int(mask_id)

    mask = CrystalMask.objects.get(pk=mask_id)
    print(mask.mask_dir)
    mask_cv = cv2.imread(mask.mask_dir)

    image = mask.image
    image_file_dir = absolute_file_dir(image.filename, IMAGE_URL)
    print("image file dir", image_file_dir)
    image_cv = cv2.imread(image_file_dir)

    crystal_cv = ps_func.show_all_crystal(image_cv, mask_cv)
    crystal_image =StateImage(func_name='', img_data=crystal_cv)
    _, image_data = cv_to_json(crystal_image)

    return JsonResponse({'image_data': image_data, 'image_name': mask.name})

def get_image_mask(mask_id):
    mask_id = int(mask_id)

    mask = CrystalMask.objects.get(pk=mask_id)
    mask_cv = cv2.imread(mask.mask_dir)
    image = mask.image
    image_file_dir = absolute_file_dir(image.filename, IMAGE_URL)
    image_cv = cv2.imread(image_file_dir)
    print("mask dir ", mask.mask_dir, "image dir ", image_file_dir)

    return mask, image_cv, mask_cv