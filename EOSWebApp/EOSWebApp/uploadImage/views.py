from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from EOSWebApp.uploadImage.forms import ImageForm
from EOSWebApp.uploadImage.models import UploadedImage


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

            file= request.FILES['image']
            print("filename", file.name, "file content type", file.content_type, "file size", file.size)
            imageDB.filename = file.name
            imageDB.user = request.user
            imageDB.save()
            return redirect('imageProcessing:processing_page', image_id=imageDB.id)
    else:
        imageForm =ImageForm()
    return render(request, 'uploadImage/upload_image.html', {'form': imageForm})

