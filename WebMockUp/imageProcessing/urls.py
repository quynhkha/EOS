from django.conf.urls import url
from imageProcessing import views

app_name ='imageProcessing'
urlpatterns = [
    #show ,
    url(r'^showImage/(?P<image_id>[0-9]+)/$', views.showImage, name='showImage'),
    url(r'^masking/$', views.masking, name='masking'),
    url(r'^dilating/$', views.dilating, name='dilating'),
    url(r'^pengzhang/$', views.pengzhang, name='pengzhang'),
    url(r'^windowing/$', views.windowing, name='windowing'),
    url(r'^ostu/$', views.ostu, name='ostu'),
    url(r'^your_name/$', views.get_name, name ='get_name'),
    url(r'^post/new/$', views.post_new, name ='post_new'),
    url(r'^success/$', views.success_message, name='success_message'),
    url(r'^base64/$', views.show_base64, name='show_base64'),
    url(r'^upload/$', views.model_form_upload, name='upload')
]