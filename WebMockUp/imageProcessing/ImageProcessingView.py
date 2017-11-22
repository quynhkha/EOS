from django.views import View
import base64
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from imageProcessing.FindSegment import FindSegment
from .forms import *
from .models import Image
from .utils import *

import copy
import cv2
from django.http import JsonResponse
from .forms import UploadFileForm
from django.views.decorators.csrf import csrf_exempt
from .imageProcessingFunc.crystal_extractor import ProcessingFunction


class ImageProcessingView(View):

    def __init__(self):
        self.processingFunction = ProcessingFunction()
        self.original_image = np.zeros((400, 400), np.uint8)
        self.current_image = np.zeros((400, 400), np.uint8)
        self.current_mask = np.zeros((400, 400), np.uint8)
        self.last_state_image = np.zeros((400, 400), np.uint8)
        self.last_state_image_arr = []
        self.history_thumbnail_arr = []
        self.max_undo_steps = 6
        self.undo_depth = 1
        self.last_called_function = ""

    @csrf_exempt
    def model_form_upload(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                file = request.FILES['document']
                print("filename", file.name, "file content type", file.content_type, "file size", file.size)
                image_file_dir = absolute_uploaded_file_dir(file.name)
                print("image file dir", image_file_dir)

                self.original_image = cv2.imread(image_file_dir)
                self.current_image = self.original_image
                self.save_state_image()
                _, image_data = cv_to_json(self.original_image)
                return render(request, 'imageProcessing/processing_page.html', {'image_data': image_data})
        else:
            form = DocumentForm()
        return render(request, 'imageProcessing/model_form_upload.html', {'form': form})

    def save_state_image(self):

        if len(self.last_state_image_arr) >= self.max_undo_steps:
            self.last_state_image_arr.pop(0)
            self.history_thumbnail_arr.pop(0)

        self.last_state_image_arr.append(self.current_image)
        self.compressed_image = self.compress_image(copy.copy(self.current_image))
        self.history_thumbnail_arr.append(self.compressed_image)

        undo_depth = len(self.last_state_image_arr) - 1

    @csrf_exempt
    def laplacian(self, request, *args, **kwargs):
        # save_state_image()
        self.current_image = self.processingFunction.laplacian_func(self.current_image)
        # json_data, _ = cv_to_json(current_image)
        self.save_state_image()
        json_data = thumbnail_plus_img_json(self.current_image, self.history_thumbnail_arr)
        return JsonResponse(json_data, safe=False)
