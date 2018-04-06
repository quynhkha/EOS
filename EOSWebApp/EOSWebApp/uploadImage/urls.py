from django.conf.urls import url

from EOSWebApp.uploadImage import views

app_name = 'uploadImage'
urlpatterns = [
url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.upload_image, name='upload'),
    url(r'^update-scale/$', views.update_image_scale, name='update scale'),
    url(r'^delete-image/(?P<image_id>[0-9]+)/$', views.delete_image, name='delete-image'),
]
