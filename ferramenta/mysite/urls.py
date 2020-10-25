from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

#from mysite.core import views
from .core import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('upload/', views.upload, name='upload'),
    path('ferramenta/', views.ferramenta, name='ferramenta'),
    path('resultado/', views.ferramenta, name='resultado'),
    path('resultadoupload/', views.upload, name='resultadoup')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
