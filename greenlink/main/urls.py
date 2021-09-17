from django.urls import path

from . import views

urlpatterns = [
    path('member/', views.ListMember.as_view()),
    path('member/<int:pk>/', views.DetailMember.as_view()),

    path('user/', views.ListUser.as_view()),
    path('user/<int:pk>/', views.DetailUser.as_view()),
    
    path('admin/', views.ListAdmin.as_view()),
    path('admin/<int:pk>/', views.DetailAdmin.as_view()),

    path('signup/', views.SignUp.as_view()),
]
