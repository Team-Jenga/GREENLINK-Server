from django.urls import path

from . import views

urlpatterns = [
    path('member/', views.ListMember.as_view()),
    path('member/<int:pk>/', views.DetailMember.as_view()),

    path('user/', views.ListUser.as_view()),
    path('user/<int:pk>/', views.DetailUser.as_view()),
    
    path('admin/', views.ListAdmin.as_view()),
    path('admin/<int:pk>/', views.DetailAdmin.as_view()),

<<<<<<< HEAD
    path('signup', views.SignUp.as_view()),
=======
    path('signup/', views.SignUp.as_view()),
>>>>>>> 4a9daf8e9cee2fd236449a3757e24dd875062f33
]
