from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, serializers

from .models import Member, MemberAdmin, MemberUser, Event
from .serializers import MemberAdminSerializer, MemberSerializer, MemberUserSerializer

import json
import bcrypt
import jwt
from django.views import View
from django.http import HttpResponse, JsonResponse
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
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Member.objects.filter(member_id = data['member_id']).exists():
                return JsonResponse({"message" : "Already Exists"}, status = 409)
            if Member.objects.filter(member_nickname = data['member_nickname']).exists():
                return JsonResponse({"message" : "Nickname Exists"}, status = 409) 
          
            Member.objects.create(
                member_id = data['member_id'],
                member_pw = bcrypt.hashpw(data["member_pw"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8"),
                member_name = data['member_name'],
                member_nickname = data['member_nickname'],
                member_auth = data['member_auth']
            ).save()
            MemberUser.objects.create(
                member_id = data['member_id'],
                member_user_birth = data['member_user_birth'],
                member_user_phone = data['member_user_phone'],
                member_user_email = data['member_user_email'],
                member_user_location = data['member_user_location'],
                member_user_num_of_family = data['member_user_num_of_family']
            ).save()

            return JsonResponse({"message" : "Success"},status = 200)

        except json.JSONDecodeError as e :
            return JsonResponse({'message': f'Json_ERROR:{e}'}, status = 400)

        except KeyError:
            return JsonResponse({"message" : "Invalid Value"}, status = 400)


class SignIn(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Member.objects.filter(member_id = data['member_id']).exists():
                user = Member.objects.get(member_id = data['member_id'])

                if bcrypt.checkpw(data['member_pw'].encode('UTF-8'), user.member_pw.encode('UTF-8')):
                    token = jwt.encode({'member_id' : user.member_id}, SECRET_KEY, 'HS256').decode('UTF-8')

                    return JsonResponse({'token' : token}, status=200)

                return JsonResponse({"message" : "Wrong Password"}, status = 400)

            return JsonResponse({"message" : "Unexist ID"}, status = 400)

        except KeyError:
            JsonResponse({"message" : "Invalid Value"}, status = 400)

            
class EventList(View):
    def get(self, request):
        event = Event.objects.all()
        event_list = serializers.serialize('json',event)
        
        return HttpResponse(event_list, content_type = "text/json-comment-filtered", status = 200)