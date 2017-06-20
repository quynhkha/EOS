from django.conf.urls import url
from imageProcessing import views

app_name ='imageProcessing'
urlpatterns = [
    #show ,
    url(r'^showImage/(?P<image_id>[0-9]+)/$', views.showImage, name='showImage'),
    url(r'^masking/$', views.masking, name='masking'),
    url(r'^dilating/$', views.dilating, name='dilating')
]