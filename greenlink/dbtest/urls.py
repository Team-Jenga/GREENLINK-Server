from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListDbtest.as_view()),
    path('<int:pk>/', views.DetailDbtest.as_view()),
]
