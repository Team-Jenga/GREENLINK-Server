from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import generics

from .models import Member, MemberAdmin, MemberUser
from .serializers import MemberAdminSerializer, MemberSerializer, MemberUserSerializer

import json
import bcrypt
from django.views import View
from greenlink.settings import SECRET_KEY

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

class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Member.objects.filter(member_id = data['member_id']).exists():
                return JsonResponse({"message" : "Already Exists"}, status=409)
            
            Member.objects.create(
                member_id = data['member_id'],
                member_pw = bcrypt.hashpw(data['member_pw'].encode('UTF-8'), bcrypt.gensalt().decode('UTF-8')),
                member_name = data['member_name'],
                member_nickname = data['member_nickname'],
                member_auth = 'user'
            ).save()

            return HttpResponse(status = 200)
        
        except KeyError:
            return JsonResponse({"message" : "Invalid Value"}, status = 400)