from django.conf.urls import url

from EOSWebApp.imageProcessing import views

app_name = 'imageProcessing'
urlpatterns = [
    # show ,
    # url(r'^showImage/(?P<image_id>[0-9]+)/$', views.showImage, name='showImage'),
    # url(r'^masking/$', views.masking, name='masking'),
    # url(r'^dilating/$', views.dilating, name='dilating'),
    # url(r'^pengzhang/$', views.pengzhang, name='pengzhang'),
    # url(r'^windowing/$', views.windowing, name='windowing'),
    # url(r'^ostu/$', views.ostu, name='ostu'),
    # url(r'^your_name/$', views.get_name, name ='get_name'),
    # url(r'^post/new/$', views.post_new, name ='post_new'),
    # url(r'^success/$', views.success_message, name='success_message'),

    url(r'^$', views.index, name='index'),
    url(r'^processing_page/(?P<image_id>[0-9]+)/$', views.processing_page, name='processing_page'),
    # url(r'^upload/$', ImageProcessingView.as_view()),
    url(r'^lower-thresholding-white/$', views.lower_thresholding_white, name='lower-thesholding-white'),
    url(r'^upper-thresholding-white/$', views.upper_thresholding_white, name='upper-thesholding-white'),
    url(r'^lower-thresholding-black/$', views.lower_thresholding_black, name='lower-thesholding-black'),
    url(r'^upper-thresholding-black/$', views.upper_thresholding_black, name='upper-thesholding-black'),
    url(r'^kmeans/$', views.kmeans, name='kmeans'),
    url(r'^laplacian/$', views.laplacian, name='laplacian'),
    url(r'^undo/$', views.undo, name="undo"),
    url(r'^fill-holes/$', views.fill_holes, name="fill-holes"),

    url(r'^extract-crystal-mask/$', views.extract_crystal_mask, name="extract-crystal-mask"),
    url(r'^all-crystal/$', views.show_all_crystal, name='show-all-crystal'),
    url(r'^top-crystal/$', views.show_top_area_crystal, name='show-max-area-crystal'),
    url(r'^reset/$', views.reset, name="reset"),
    url(r'^img-from-thumbnail/$', views.set_image_from_thumbnail, name="img-from-thumbnail"),
    #
    url(r'^opening/$', views.do_opening, name='opening'),
    url(r'^closing/$', views.do_closing, name='closing'),
    url(r'^erosion/$', views.do_erosion, name='erosion'),
    url(r'^dilation/$', views.do_opening, name='dilation'),
    url(r'^morphgrad/$', views.do_morphgrad, name='morphgrad'),
    url(r'^tophat/$', views.do_tophat, name='tophat'),
    url(r'^blackhat/$', views.do_blackhat, name='blackhat'),
    #
    url(r'^update-mask/$', views.update_mask, name='update-mask'),
    url(r'^noise-removal/$', views.noise_removal, name='noise-removal'),
    url(r'^save-processed/$', views.save_processed, name='save-processed'),
    url(r'^delete-image/(?P<image_id>[0-9]+)/$', views.delete_image, name='delete-image'),
    #
    # url(r'^fourier/$', views.do_fourier, name='fourier'),
    # url(r'^backproj/$', views.do_backproj, name='backproj'),
    url(r'^large-thumbnail/(?P<thumbnail_id>[0-9]+)/$', views.large_thumbnail, name='large-thumbnail')
]
