from django.contrib import admin
from app import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tableId', views.index),
    path('callW', views.send_html_message),
]


