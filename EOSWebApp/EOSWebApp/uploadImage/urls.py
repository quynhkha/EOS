from django.conf.urls import url

from EOSWebApp.uploadImage import views

app_name = 'uploadImage'
urlpatterns = [
url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload_image, name='upload'),

]