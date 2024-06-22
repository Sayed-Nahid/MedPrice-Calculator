import os
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ImageForm, ImageUploadForm
from .models import Image
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.conf import settings
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Construct the full path to your model file
model_path = os.path.join(settings.BASE_DIR, 'myapp/static/myapp/drugs_model.h5')
model = load_model(model_path)

# Define the class labels dictionary and reverse dictionary
label_dict = {'amodis_400_1': 0, 'amodis_400_10': 1, 'amodis_400_2': 2, 'amodis_400_3': 3, 'amodis_400_4': 4, 'amodis_400_5': 5, 'amodis_400_6': 6, 'amodis_400_7': 7, 'amodis_400_8': 8, 'amodis_400_9': 9, 'artica_10_1': 10, 'artica_10_10': 11, 'artica_10_2': 12, 'artica_10_3': 13, 'artica_10_4': 14, 'artica_10_5': 15, 'artica_10_6': 16, 'artica_10_7': 17, 'artica_10_8': 18, 'artica_10_9': 19, 'doxiva_200_1': 20, 'doxiva_200_10': 21, 'doxiva_200_2': 22, 'doxiva_200_3': 23, 'doxiva_200_4': 24, 'doxiva_200_5': 25, 'doxiva_200_6': 26, 'doxiva_200_7': 27, 'doxiva_200_8': 28, 'doxiva_200_9': 29, 'flexor_5_1': 30, 'flexor_5_10': 31, 'flexor_5_2': 32, 'flexor_5_3': 33, 'flexor_5_4': 34, 'flexor_5_5': 35, 'flexor_5_6': 36, 'flexor_5_7': 37, 'flexor_5_8': 38, 'flexor_5_9': 39, 'montene_10_1': 40, 'montene_10_10': 41, 'montene_10_2': 42, 'montene_10_3': 43, 'montene_10_4': 44, 'montene_10_5': 45, 'montene_10_6': 46, 'montene_10_7': 47, 'montene_10_8': 48, 'montene_10_9': 49, 'napa_1': 50, 'napa_10': 51, 'napa_2': 52, 'napa_3': 53, 'napa_4': 54, 'napa_5': 55, 'napa_6': 56, 'napa_7': 57, 'napa_8': 58, 'napa_9': 59, 'napa_extra_1': 60, 'napa_extra_10': 61, 'napa_extra_11': 62, 'napa_extra_12': 63, 'napa_extra_2': 64, 'napa_extra_3': 65, 'napa_extra_4': 66, 'napa_extra_5': 67, 'napa_extra_6': 68, 'napa_extra_7': 69, 'napa_extra_8': 70, 'napa_extra_9': 71, 'sergel_1': 72, 'sergel_2': 73, 'sergel_3': 74, 'sergel_4': 75, 'sergel_5': 76, 'sergel_6': 77, 'sergel_7': 78, 'sergel_8': 79, 'sergel_9': 80}
reverse_label_dict = {v: k for k, v in label_dict.items()}


class HomePage(View):
    def get(self, request):
        form = ImageUploadForm()
        return render(request, 'index.html', {'form': form})

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img_file = form.cleaned_data['image']
            img = Image.open(img_file)
            img = img.resize((200, 200))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            img_array /= 255.0  # Normalize as per your model requirement

            # Predict the class
            predictions = model.predict(img_array)
            predicted_class = np.argmax(predictions, axis=1)

            predicted_class_index = np.argmax(predictions, axis=1)[0]
            predicted_class_label = reverse_label_dict[predicted_class_index]

            return JsonResponse({'predicted_class': predicted_class_label})

        return JsonResponse({'error': 'Invalid form'}, status=400)

def contactPage(request):
    pageInfo={
        'title': 'Contact Page'
    }
    return render(request, "contact.html", pageInfo)

def aboutPage(request):
    pageInfo={
        'title': 'About Page'
    }
    return render(request, "about.html", pageInfo)

class ImageUploadView(View):
    def get(self, request):
        form = ImageUploadForm()
        return render(request, 'upload.html', {'form': form})

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img_file = form.cleaned_data['image']
            img = Image.open(img_file)
            img = img.resize((200, 200))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            img_array /= 255.0  # Normalize as per your model requirement

            # Predict the class
            predictions = model.predict(img_array)
            predicted_class = np.argmax(predictions, axis=1)

            predicted_class_index = np.argmax(predictions, axis=1)[0]
            predicted_class_label = reverse_label_dict[predicted_class_index]

            return JsonResponse({'predicted_class': predicted_class_label})

        return JsonResponse({'error': 'Invalid form'}, status=400)

