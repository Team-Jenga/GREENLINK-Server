from django.urls import path

from . import views
from .views import EventList, SignUp, SignIn

urlpatterns = [
    path('member/', views.ListMember.as_view()),
    path('member/<int:pk>/', views.DetailMember.as_view()),

    path('user/', views.ListUser.as_view()),
    path('user/<int:pk>/', views.DetailUser.as_view()),
    
    path('admin/', views.ListAdmin.as_view()),
    path('admin/<int:pk>/', views.DetailAdmin.as_view()),

    path('signup', SignUp.as_view()),
    path('signin', SignIn.as_view()),

    path('notice', views.ListNotice.as_view(), name='notice_list'),
    path('notice/<int:pk>', views.DetailNotice.as_view(), name='notice_detail'),
    path('eventlist', EventList.as_view()),
]
