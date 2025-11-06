from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('numbers/', include('apps.visualnumbers.urls',namespace='numbers')),
    path('', include('apps.main.urls',namespace='main')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
