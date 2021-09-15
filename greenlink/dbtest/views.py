from django.shortcuts import render
from rest_framework import generics

from .models import Dbtest
from .serializers import DbtestSerializer

class ListDbtest(generics.ListCreateAPIView):
    queryset = Dbtest.objects.all()
    serializer_class = DbtestSerializer

class DetailDbtest(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dbtest.objects.all()
    serializer_class = DbtestSerializer