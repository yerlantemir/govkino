from django.urls import path
from rest_framework.authtoken import views as authview

from . import views

urlpatterns = [
    path('', views.event_list, name="getpost"),
    path('<int:pk>/', views.event_detail, name="detail"),
    path('configuration/<int:pk>/', views.event_action, name="config")
]