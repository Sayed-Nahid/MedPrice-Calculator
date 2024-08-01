import os
import json
import base64
import requests
from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from django.core.files.storage import FileSystemStorage
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.conf import settings
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from ultralytics import YOLO

count_model_path = os.path.join(settings.BASE_DIR, 'myapp/static/myapp/count.pt')
count_model = YOLO(count_model_path)

model_path = os.path.join(settings.BASE_DIR, 'myapp/static/myapp/drugs_model_v0.3.h5')
model = load_model(model_path)

label_path = os.path.join(settings.BASE_DIR, 'myapp/static/myapp/label_map.json')
with open(label_path, 'r') as f:
    label_map = json.load(f)

reverse_label_dict = {v: k for k, v in label_map.items()}

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return (str(o))
        return json.JSONEncoder.default(self, obj)

class HomePage(View):
    def get(self, request):
        try:
            del request.session['cart_id']
        except:
            print("Session variable 'cart_id' does not exist")

        return render(request, 'index.html')

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

def inventory(request):
    products = Product.objects.all()
    return render(request, "inventory.html", {'items': products})

def capture_image(request):
    cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id'))
    if created:
        request.session['cart_id'] = cart.id

    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        file_url = fs.url(filename)

        print("filename", filename)
        print("filename path", fs.path(filename))
        print("file url", file_url)

        classification, quantity = classify_image(fs.path(filename))

        image_classification = ImageClassification(
            image=filename,
            output_class=classification
        )
        image_classification.save()

        name_slug = classification

        product_name = name_slug.replace('_', ' ').capitalize()

        product = Product.objects.get(slug=name_slug, name=product_name)

        cart_item = CartItem(cart=cart, product=product, quantity=quantity, image_class=image_classification)
        # cart_item.quantity += quantity
        cart_item.save()

        response_data = {
            'class_id': image_classification.id,
            'image_url': file_url,
            'output_class': classification,
            'cart_id': cart.id
        }
        items = cart.items.all().order_by('-image_class__uploaded_at')
        total = 0
        for item in items:
            total += float(item.product.price * item.quantity)
        items_data = [
            {
                'id': item.id,
                'image_url': item.image_class.image.url,
                'product_name': item.product.name,
                'product_slug': item.product.slug,
                'quantity_in_stock': item.product.quantity_in_stock,
                'unit_price': str(item.product.price),
                'price': str(item.product.price * item.quantity),
                'quantity': item.quantity,
            }
            for item in items
        ]
        print(json.dumps(items_data))
        return JsonResponse({'data': items_data, 'total': str(total)})
        # return JsonResponse(response_data)
    else:
        if created:
            status = "empty"
        cart_items = cart.items.all().order_by('-image_class__uploaded_at')
        if len(cart_items) == 0:
            status = "empty"
        else:
            status = "available"
        data = []
        total = 0
        for item in cart_items:
            data.append({
                'id': item.id,
                'image_url': item.image_class.image.url,
                'product_name': item.product.name,
                'product_slug': item.product.slug,
                'unit_price': str(item.product.price),
                'price': str(item.product.price * item.quantity),
                'quantity': item.quantity,
                'quantity_in_stock': item.product.quantity_in_stock,
            })
            total += item.product.price * item.quantity
        return render(request, "capture.html", {'items': data, 'cart': cart, 'total': total, 'status': status})

def checkout(request):
    print("checkout page")
    cart_id = request.session.get('cart_id')
    if not cart_id:
        return JsonResponse({'error': 'Cart not found'}, status=404)

    if request.method == 'POST':
        try:
            del request.session['cart_id']
        except:
            print("Session variable 'cart_id' does not exist")
        return redirect('capture_image')
    else:
        cart = Cart.objects.get(id=cart_id)
        cart_items = cart.items.all().order_by('-image_class__uploaded_at')
        if len(cart_items) == 0:
            status = "empty"
        else:
            status = "available"
        data = []
        total = 0
        for item in cart_items:
            data.append({
                'id': item.id,
                'image_url': item.image_class.image.url,
                'product_name': item.product.name,
                'product_slug': item.product.slug,
                'unit_price': str(item.product.price),
                'price': str(item.product.price * item.quantity),
                'quantity': item.quantity,
                'quantity_in_stock': item.product.quantity_in_stock,
            })
            if int(item.quantity) <= int(item.product.quantity_in_stock):
                print("condition true")
                print(item.product.quantity_in_stock)
                try:
                    item.product.quantity_in_stock = int(item.product.quantity_in_stock) - int(item.quantity)
                    item.product.save()
                    print("update success")
                    print(item.product.quantity_in_stock)
                except: 
                    print("Quantity mismatch with stock")
            total += item.product.price * item.quantity
        return render(request, "checkout.html", {'items': data, 'cart': cart, 'total': total, 'status': status})

def delete_cart_item(request, id):
    if request.method == 'POST':
        try:
            cart_item = CartItem.objects.get(id=id)
            cart_item.delete()

            cart_items = CartItem.objects.all()  # Adjust as needed to filter by user, session, etc.
            data = []
            total_price = 0

            cart = Cart.objects.get(id=request.session.get('cart_id'))
            cart_items = cart.items.all().order_by('-image_class__uploaded_at')

            for item in cart_items:
                data.append({
                    'id': item.id,
                    'image_url': item.image_class.image.url,
                    'product_name': item.product.name,
                    'product_slug': item.product.slug,
                    'unit_price': str(item.product.price),
                    'price': str(item.product.price * item.quantity),
                    'quantity': item.quantity,
                    'quantity_in_stock': item.product.quantity_in_stock,
                })
                total_price += item.product.price * item.quantity

            return JsonResponse({'data': data, 'total': str(total_price)})
        
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def classify_image(image_path):
    img = Image.open(image_path)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img = img.resize((480, 480))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0

    qty_result = count_model(image_path)
    quantity = len(qty_result[0].boxes)

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)

    class_index = np.argmax(predictions, axis=1)[0]
    label = reverse_label_dict[class_index]
    return label, quantity

def correct_class(request, image_id):
    if request.method == 'POST':
        corrected_class = request.POST.get('corrected_class')
        image_classification = get_object_or_404(ImageClassification, pk=image_id)
        image_classification.corrected_class = corrected_class
        image_classification.save()
        return render(request, 'corrected.html', {'classification': image_classification})

def cart_detail(request):
    cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id'))
    if created:
        request.session['cart_id'] = cart.id
    return render(request, 'cart_detail.html', {'cart': cart})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(id=request.session.get('cart_id'))
    if created:
        request.session['cart_id'] = cart.id

    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += form.cleaned_data['quantity']
            cart_item.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def update_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity'))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        return JsonResponse({'success': True, 'quantity': cart_item.quantity, 'total_price': cart_item.total_price()})

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return JsonResponse({'success': True})

