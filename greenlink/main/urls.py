from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListMain.as_view()),
    path('<int:pk>/', views.DetailMain.as_view()),
]