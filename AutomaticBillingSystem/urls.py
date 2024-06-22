from django.contrib import admin
from django.urls import include, path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePage.as_view()),
    path('contact/', views.contactPage),
    path('about/', views.aboutPage),
    path('', include('myapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

