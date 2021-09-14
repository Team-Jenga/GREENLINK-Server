from django.shortcuts import render
from rest_framework import generics

from .models import Main
from .serializers import MainSerializer

class ListMain(generics.ListCreateAPIView):
    queryset = Main.objects.all()
    serializer_class = MainSerializer

class DetailMain(generics.RetrieveUpdateDestroyAPIView):
    queryset = Main.objects.all()
    serializer_class = MainSerializer
