from django.urls import path

from . import views

urlpatterns = [
    path('all_cases', views.TodoListApiView.as_view()),
    path('case/<int:pk>', views.TodoOnceView.as_view()),
    path("cases/", views.TodoListCreateAPIView.as_view()),
    path("public_cases/", views.TodoPublicListApiView.as_view()),
    path("filter_cases/", views.TodoListFilterApiView.as_view()),
    path("edit_case/<int:pk>", views.TodoEditViaGeneric.as_view()),

]