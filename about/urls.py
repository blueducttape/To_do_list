from django.urls import path, include
from . import views

urlpatterns = [
    path('about', views.IndexView.as_view()),
]