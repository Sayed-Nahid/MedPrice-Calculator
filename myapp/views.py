from django.http import HttpResponse
from django.shortcuts import render
from .forms import ImageForm
from .models import Image
def homePage(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    pageInfo={
        'title': 'Home Page'
    }
    form = ImageForm()
    return render(request, "index.html", {'form':form})

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