from django.urls import path

from . import views
from .views import CheckDupleID, CheckDupleNick, FindID, FindPW, ListEvent, SearchEvent, SendAuth, SignUp, SignIn

urlpatterns = [
    path('member/<str:pk>', views.DetailMember.as_view()),
    path('member/<str:pk>/changepw', views.ChangePW.as_view()),

    path('eventlist', views.ListEvent.as_view()),

    path('signup', SignUp.as_view()),
    path('signin', SignIn.as_view()),
    path('sendauth', SendAuth.as_view()),
    path('checkid', CheckDupleID.as_view()),
    path('checknick', CheckDupleNick.as_view()),

    path('findid', FindID.as_view()),
    path('findpw', FindPW.as_view()),

    path('notice', views.ListNotice.as_view()),
    path('notice/<int:pk>', views.DetailNotice.as_view()),

    path('event', views.ListEvent.as_view()), 
    path('event/<int:pk>/',views.DetailEvent.as_view()),
    path('eventsearch',views.SearchEvent.as_view())
]
