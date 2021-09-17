from django.shortcuts import render
from rest_framework import generics

from .models import Member, MemberAdmin, MemberUser
from .serializers import MemberAdminSerializer, MemberSerializer, MemberUserSerializer

class ListMember(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class DetailMember(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class ListUser(generics.ListCreateAPIView):
    queryset = MemberUser.objects.all()
    serializer_class = MemberUserSerializer

class DetailUser(generics.RetrieveUpdateDestroyAPIView):
    queryset = MemberUser.objects.all()
    serializer_class = MemberUserSerializer

class ListAdmin(generics.ListCreateAPIView):
    queryset = MemberAdmin.objects.all()
    serializer_class = MemberAdminSerializer

class DetailAdmin(generics.RetrieveUpdateDestroyAPIView):
    queryset = MemberAdmin.objects.all()
    serializer_class = MemberAdminSerializer

def index(request):
    return render(request, "main/index.html")