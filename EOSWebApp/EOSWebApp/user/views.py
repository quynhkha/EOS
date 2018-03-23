from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from EOSWebApp.imageProcessing.models import UploadedImage
from EOSWebApp.user.forms import UserForm
from EOSWebApp.utils import shared_data

temp_data_arr = shared_data.temp_data_arr

@csrf_exempt
def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False) # create a user object but does not save it to DB yet
        # clean (normalized) the data
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password) # need to set password in this way because password is stored as encrypted text
        user.save()

        # return User object it credentials are correct
        user = authenticate(username=username, password = password)

        return render(request, 'user/login.html')
        # if user is not None:
        #     if user.is_active:

    context = {
        "form": form,
    }

    return render(request, 'user/register.html', context)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)


        if user is not None:
            if user.is_active:
                login(request, user)

                # return render(request, 'imageProcessing/index.html', {'user': user})
                return redirect('imageProcessing:index')
            else:
                return render(request, 'error.html', {'error_message': "Your account has been deactivated"})
        else:
            return render(request, 'user/login.html', {'error_message:': "Invalid login"})
    return render(request, 'user/login.html')


def logout_user(request):

    # TODO: clear user's temp data
    global temp_data_arr
    try:
        for temp in temp_data_arr:
            if temp.user_id == request.session['user_id'] and temp.image_id == request.session['image_id']:
                temp_data_arr.remove(temp)
    except KeyError:
        pass
    print('temp_data_arr', temp_data_arr)

    # try:
    #
    #     uploaded_images = UploadedImage.objects.filter(user=request.user)
    #     for uploaded_image in uploaded_images:
    #         temp_images = TempImage.objects.filter(image)
    # Flush session info
    try:
        del request.session['user_id']
        if request.session['image_id'] is not None:
            del request.session['image_id']
    except KeyError:
        pass

    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }

    return render(request, 'user/login.html', context)