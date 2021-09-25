from django.db.models import query
from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics

from .models import  EventDetail, Member, MemberAdmin, MemberUser, Event, Notice
from .serializers import MemberAdminSerializer, MemberSerializer, MemberUserSerializer, EventSerializer, NoticeSerializer

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

class ListEvent(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


def index(request):
    return render(request, "main/index.html")

class SignUp(View):
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Member.objects.filter(member_id = data['member_id']).exists():
                return JsonResponse({"message" : "Id Already Exists"}, status = 408)
            if Member.objects.filter(member_nickname = data['member_nickname']).exists():
                return JsonResponse({"message" : "Nickname Aleady Exists"}, status = 409) 
          
            Member.objects.create(
                member_id = data['member_id'],
                member_pw = bcrypt.hashpw(data["member_pw"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8"),
                member_name = data['member_name'],
                member_nickname = data['member_nickname'],
                member_auth = data['member_auth']
            ).save()

            if data['member_auth'] == 'user':
                MemberUser.objects.create(
                    member_id = data['member_id'],
                    member_user_birth = data['member_user_birth'],
                    member_user_phone = data['member_user_phone'],
                    member_user_email = data['member_user_email'],
                    # member_user_location = data['member_user_location'],
                    # member_user_num_of_family = data['member_user_num_of_family']
                ).save()
            elif data['member_auth'] == 'admin':
                MemberAdmin.objects.create(
                    member_id = data['member_id'],
                    member_admin_position = 1
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

class CheckDupleID(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Member.objects.filter(member_id = data['member_id']).exists():
                return JsonResponse({"status": "200", "message" : "false"},status = 200)
            else:
                return JsonResponse({"status": "200", "message" : "true"},status = 200)  

        except json.JSONDecodeError as e :
            return JsonResponse({'message': f'Json_ERROR:{e}'}, status = 400)
        except KeyError:
            return JsonResponse({"message" : "Invalid Value"}, status = 400)

class CheckDupleNick(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Member.objects.filter(member_nickname = data['member_nickname']).exists():
                return JsonResponse({"status": "200", "message" : "false"},status = 200)
            else:
                return JsonResponse({"status": "200", "message" : "true"},status = 200)  
                

        except json.JSONDecodeError as e :
            return JsonResponse({'message': f'Json_ERROR:{e}'}, status = 400)
        except KeyError:
            return JsonResponse({"message" : "Invalid Value"}, status = 400)

class ListNotice(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

class DetailNotice(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    
    def get(self, request, *args, **kwargs):
        item = Notice.objects.get(pk=kwargs['pk'])
        item.notice_views += 1
        item.save()

        return super().get(request, *args, **kwargs)


class CreateEvent(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            Event.objects.create(
                member_id = data['member_id'],
                event_title = data['event_title'],
                event_location = data['event_location'],
                event_views = 0
            ).save()
            
            EventDetail.objects.create(
                event = Event.objects.latest("event_id"),
                event_management =  data['event_management'],
                event_period_start =  data['event_period_start'],
                event_period_end =  data['event_period_end'],
                event_url = data['event_url'],
                event_image_url =  data['event_image_url'],
                event_content = data['event_content'],
            ).save()

            return JsonResponse({"message" : "Success"}, status = 200)

        except json.JSONDecodeError as e :
            return JsonResponse({'message': f'Json_ERROR:{e}'}, status = 400)

        except KeyError:
            return JsonResponse({"message" : "Invalid Value"}, status = 400)
