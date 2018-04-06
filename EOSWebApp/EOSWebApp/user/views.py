from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from EOSWebApp.imageProcessing.models import UploadedImage
from EOSWebApp.imageProcessing.utils import get_state_data, find_state_data
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
                return redirect('uploadImage:index')
            else:
                return render(request, 'error.html', {'error_message': "Your account has been deactivated"})
        else:
            return render(request, 'user/login.html', {'error_message:': "Invalid login"})
    return render(request, 'user/login.html')


def logout_user(request):
    try:
        images = UploadedImage.objects.filter(user=request.user)
        for image in images:
            try:
                state_data = find_state_data(temp_data_arr, image.id)

                if state_data is not None:
                    print('image_id', state_data.s_img_ori_id)
                    state_data.delete_hist_imgs()
                    temp_data_arr.remove(state_data)

            except:
                raise
        print('temp_data_arr', temp_data_arr)
        try:
            del request.session['user_id']
            del request.session['image_id']
        except:
            pass
        logout(request)

    except:
        pass
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }

    return render(request, 'user/login.html', context)