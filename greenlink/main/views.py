from django.shortcuts import render
from rest_framework import generics

from .models import Member
from .serializers import MemberSerializer

class ListMember(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class DetailMember(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

def index(request):
    return render(request, "main/index.html")