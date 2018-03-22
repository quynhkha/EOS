from django.conf.urls import url

from EOSWebApp.crystalManagement import views

app_name = 'crystalManagement'
urlpatterns = [

    url(r'^modal-show-crystal/(?P<mask_id>[0-9]+)/$', views.modal_show_crystal, name='modal-show-crystal'),
    url(r'^modal-show-individual-crystal/(?P<crystal_id>[0-9]+)/$', views.modal_show_individual_crystal, name='modal-show-individual-crystal'),
    url(r'^modal-show-conf-graph/(?P<i>[0-9]+)/$', views.modal_show_conf_graph,
        name='modal-show-conf-graph'),
    url(r'^download-crystal/(?P<mask_id>[0-9]+)/$', views.download_crystal, name='download-crystal'),
    url(r'^delete-mask/(?P<mask_id>[0-9]+)/$', views.delete_mask, name='delete-mask'),
    url(r'^library/$', views.library_page, name='library'),
    url(r'^histogram/(?P<mask_id>[0-9]+)/$', views.plot_histogram, name="plot-histogram"),
    # url(r'^crystal_processing/(?P<mask_id>[0-9]+)/$', views.crystal_processing_page, name="crystal-processing-page"),
url(r'^crystal_processing/$', views.crystal_processing_page, name="crystal-processing-page"),
    url(r'^gen-crystal-processing-result/$', views.gen_crystal_processing_result, name='gen-crystal-processing-result')

]
