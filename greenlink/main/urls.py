from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListMember.as_view()),
    path('<int:pk>/', views.DetailMember.as_view()),
]
