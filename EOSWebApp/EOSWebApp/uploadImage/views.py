import cv2
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from EOSWebApp.uploadImage.forms import ImageForm
from EOSWebApp.uploadImage.models import UploadedImage
from EOSWebApp.utils import cv_to_json


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
        image_form = ImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            uploaded_image = image_form.save()

            file= request.FILES['image']
            print("filename", file.name, "file content type", file.content_type, "file size", file.size)
            uploaded_image.filename = file.name
            uploaded_image.user = request.user
            uploaded_image.save()

            # need to pass base64 image instead of img url because some images are in tif format which is non-displayable
            # by html <img src=""> method
            image_cv = cv2.imread(uploaded_image.image.path)
            _, image_data = cv_to_json(image_cv)
            # return redirect('imageProcessing:processing_page', image_id=imageDB.id)
            return render(request, 'uploadImage/update_image_scale.html', {'image_data': image_data, 'image_id': uploaded_image.id})
    else:
        image_form =ImageForm()
    return render(request, 'uploadImage/upload_image.html', {'form': image_form})

@csrf_exempt
def update_image_scale(request):
    pixel_dist = int(request.POST.get('pixel_dist'))
    real_dist = int(request.POST.get('real_dist'))
    image_id = int(request.POST.get('image_id'))

    image = UploadedImage.objects.get(pk=image_id)
    image.dist_per_pixel = float(real_dist/pixel_dist)
    image.save()

    json_data = {'status': 'success'}
    return JsonResponse(json_data)



@csrf_exempt
def delete_image(request, image_id):
    image_id = int(image_id)
    image = UploadedImage.objects.get(pk=image_id)
    image.delete()
    images = UploadedImage.objects.filter(user=request.user)
    return render(request, 'index.html', {'user': request.user, 'images': images})


