from django.conf.urls import url

from EOSWebApp.crystalManagement import views

app_name = 'crystalManagement'
urlpatterns = [

    url(r'^modal-show-crystal/(?P<mask_id>[0-9]+)/$', views.modal_show_crystal, name='modal-show-crystal'),
    url(r'^download-crystal/(?P<mask_id>[0-9]+)/$', views.download_crystal, name='download-crystal'),
    url(r'^delete-mask/(?P<mask_id>[0-9]+)/$', views.delete_mask, name='delete-mask'),
    url(r'^library/$', views.library_page, name='library'),
]
