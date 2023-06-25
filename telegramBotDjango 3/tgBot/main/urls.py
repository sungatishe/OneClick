from django.urls import path
from . import views

urlpatterns = [
    path('tableId', views.index),
    path('callW', views.send_html_message)
]
