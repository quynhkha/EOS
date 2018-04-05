from django.conf.urls import url

from EOSWebApp.uploadImage import views

app_name = 'uploadImage'
urlpatterns = [

    url(r'^upload/$', views.upload_image, name='upload'),

]
