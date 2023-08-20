"""
URL configuration for senal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from my_app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('test', views.testing, name='testing'),
    path('probar', views.test, name='test'),
    path('onDriver', views.activateDriver, name='onDriver'),
    path('getPosts', views.getContent, name='getContent'),
    path('getUrl/<str:href>', views.get_url, name='getUrl'),
    path('file', views.file, name='file')

]

# Agrega esto al final para manejar las URL de archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)