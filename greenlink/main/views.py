from django.db import connection
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.views import APIView

from .models import Member, MemberAdmin, MemberUser, Event, Favorite, Notice
from .serializers import MemberSerializer, EventSerializer, FavoriteSerializer, NoticeSerializer

import json
import bcrypt
import jwt
import random, secrets, string, datetime
from django.views import View
from django.http import JsonResponse
from greenlink.settings import SECRET_KEY
from django.core.mail import EmailMessage

class DetailMember(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def get(self, request, *args, **kwargs):
        try:
            member_info = Member.objects.filter(member_id = kwargs['pk'])
            member_user_info = MemberUser.objects.all().filter(member = kwargs['pk'])

            return JsonResponse({"status": 200, 'info': list(member_info.values()) + list(member_user_info.values())}, status = 200)
        except KeyError:
            return JsonResponse({"message" : "Invalid Value"}, status = 400)

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            item = Member.objects.get(pk=kwargs['pk'])
            item.member_nickname = data['member_nickname']
            item.save()
            item = MemberUser.objects.get(pk=kwargs['pk'])
            item.member_user_birth = data['member_birth']
            item.member_user_phone = data['member_phone']
            item.member_user_email = data['member_email']
            item.member_user_location = data['member_location']
            item.member_user_num_of_family = data['member_num_of_family']
            item.save()

            return JsonResponse({"status": 200, "message" : "Success"}, status = 200)
        except KeyError:
            return JsonResponse({"message" : "Invalid Value"}, status = 400)

class ChangePW(generics.RetrieveUpdateDestroyAPIView):
    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            item = Member.objects.get(pk=kwargs['pk'])
            item.member_pw = bcrypt.hashpw(data["member_pw"].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")
            item.save()

            return JsonResponse({"status": 200, "message" : "Success"}, status = 200)
        except KeyError:
            return JsonResponse({"message" : "Invalid Value"}, status = 400)
         
class ListEvent(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        cur = connection.cursor()

        cur.execute("ALTER TABLE event AUTO_INCREMENT=1")
        cur.execute("SET @COUNT = 0")
        cur.execute("UPDATE event SET event_id = @COUNT:=@COUNT+1")
        
        cur.fetchall()

        connection.commit()
        connection.close()

        try:
            queryset = Event.objects.all().order_by('-event_id')
            order_by = request.GET.get('order_by', None)
            if order_by == 'hits':
                queryset = Event.objects.all().order_by('-event_views')
            return JsonResponse({'status' : 200, 'event_list': list(queryset.values())}, status = 200)
        except KeyError:
            return JsonResponse({"status": 400, "message" : "Invalid Value"}, status = 400)

class DetailEvent(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        item = Event.objects.get(pk=kwargs['pk'])
        item.event_views += 1
        item.save()

        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        dt_now = datetime.datetime.now()
        item = Notice.objects.get(pk=kwargs['pk'])
        item.created_at = dt_now
        item.save()

        return super().put(request, *args, **kwargs)
    
class SearchEvent(APIView):
    def get(self, request):
        queryset = Event.objects.all()
        
        search_key = request.GET.get('search_key', None)
        if search_key:
            event_list = queryset.filter(event_title__icontains = search_key)

            return JsonResponse({'status' : 200, 'event_list': list(event_list.values())}, status = 200)
        else: 
            return JsonResponse({'status': 400, 'message' :'Search failed'}, status = 400)


class ListFavorite(generics.CreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def get(self, request):
        try:
            cur = connection.cursor()

            cur.execute("ALTER TABLE favorite AUTO_INCREMENT=1")
            cur.execute("SET @COUNT = 0")
            cur.execute("UPDATE favorite SET id = @COUNT:=@COUNT+1")
            
            cur.fetchall()

            connection.commit()
            connection.close()

            response = []
            member = request.GET.get('member', None)
            favorite_instance = list(Favorite.objects.filter(member_id = member).values())
            
            for instance in favorite_instance:
                event_instance = list(Event.objects.filter(event_id = instance['event_id']).values())[0]
                response.append(event_instance)

            return JsonResponse({'status' : 200, 'event_list': response}, status = 200)
        except KeyError:
            return JsonResponse({'status' : 400, 'message' : "Invalid Value"}, status = 400)

    def delete(self, request):
        data = json.loads(request.body)

        try:
            Favorite.objects.filter(member_id = data['member'], event_id = data['event']).delete()

            return JsonResponse({'status' : 200, 'message' : "Completely Delete"}, status = 200)
        except:
            return JsonResponse({'status' : 400, 'message' : "Fail to delete"}, status = 400)

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

            return JsonResponse({"status": 200, "message" : "Success"},status = 200)

        except json.JSONDecodeError as e :
            return JsonResponse({"status": 400, 'message': f'Json_ERROR:{e}'}, status = 400)

        except KeyError:
            return JsonResponse({"status": 400, "message" : "Invalid Value"}, status = 400)

class SendAuth(APIView):
    def post(self, request):
        email = request.data['member_email']

        try:
            subject = 'Greenlink 회원가입 인증 안내 입니다.'
            number = random.randrange(10000,100000)
            message = str(number)
            mail = EmailMessage(subject, message, to=[email])
            mail.send()
            
            return JsonResponse({"status": 200, "message" : message}, status = 200)

        except KeyError:
            return JsonResponse({"status": 400, "message" : "Invalid Value"}, status = 400)

class SignIn(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Member.objects.filter(member_id = data['member_id']).exists():
                user = Member.objects.get(member_id = data['member_id'])

                if bcrypt.checkpw(data['member_pw'].encode('UTF-8'), user.member_pw.encode('UTF-8')):
                    token = jwt.encode({'member_id' : user.member_id}, SECRET_KEY, 'HS256').decode('UTF-8')

                    return JsonResponse({"status": 200, 'token' : token,'auth' : user.member_auth}, status=200)

                return JsonResponse({"status": 201, "message" : "Wrong Password"}, status = 201)

            return JsonResponse({"status": 202, "message" : "Unexist ID"}, status = 202)

        except KeyError:
            JsonResponse({"message" : "Invalid Value"}, status = 400)

class CheckDupleID(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Member.objects.filter(member_id = data['member_id']).exists():
                return JsonResponse({"status": 200, "message" : "false"},status = 200)
            else:
                return JsonResponse({"status": 200, "message" : "true"},status = 200)  

        except json.JSONDecodeError as e :
            return JsonResponse({'message': f'Json_ERROR:{e}'}, status = 400)
        except KeyError:
            return JsonResponse({"message" : "Invalid Value"}, status = 400)

class CheckDupleNick(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Member.objects.filter(member_nickname = data['member_nickname']).exists():
                return JsonResponse({"status": 200, "message" : "false"},status = 200)
            else:
                return JsonResponse({"status": 200, "message" : "true"},status = 200)  
                

        except json.JSONDecodeError as e :
            return JsonResponse({'message': f'Json_ERROR:{e}'}, status = 400)
        except KeyError:
            return JsonResponse({"message" : "Invalid Value"}, status = 400)

class FindID(APIView):
    def post(self, request):
        email = request.data['member_email']

        try:
            if MemberUser.objects.filter(member_user_email = email).exists():
                member = MemberUser.objects.get(member_user_email = email)
                return JsonResponse({"status": 200, "message" : str(member)}, status = 200)
            else:
                return JsonResponse({"status": 201, "message" : "email doesn't exist"}, status = 201)

        except KeyError:
            return JsonResponse({"status": 400, "message" : "Invalid Value"}, status = 400)

class FindPW(APIView):
    def post(self, request):
        member_id_ = request.data['member_id']

        try:
            if Member.objects.filter(member_id = member_id_).exists():
                member_email = MemberUser.objects.get(member=member_id_).member_user_email

                subject = 'Greenlink 회원님의 임시 비밀번호입니다.'
                string_pool = string.ascii_letters + string.digits
                while True:
                    temp_password = ''.join(secrets.choice(string_pool) for i in range(10))
                    if (any(c.islower() for c in temp_password)
                    and any(c.isupper() for c in temp_password)
                    and sum(c.isdigit() for c in temp_password) >= 3):
                        break
                message = str(temp_password)

                Member.objects.filter(member_id = member_id_).update(
                    member_pw = bcrypt.hashpw(message.encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8"),
                )

                mail = EmailMessage(subject, message, to=[member_email])
                mail.send()
                return JsonResponse({"status": 200, "message" : 'Success'}, status = 200)
            else:
                return JsonResponse({"status": 201, "message" : "ID doesn't exist"}, status = 201)

        except KeyError:
            return JsonResponse({"status": 400, "message" : "Invalid Value"}, status = 400)

class ListNotice(generics.ListCreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    def get(self, request, *args, **kwargs):
        cur = connection.cursor()
        
        cur.execute("ALTER TABLE notice AUTO_INCREMENT=1")
        cur.execute("SET @COUNT = 0")
        cur.execute("UPDATE notice SET id = @COUNT:=@COUNT+1")
        cur.fetchall()

        connection.commit()
        connection.close()
        
        try:
            queryset = Notice.objects.all().order_by('-id')
            return JsonResponse({'status' : 200, 'data': list(queryset.values())}, status = 200)
        except KeyError:
            return JsonResponse({"status": 400, "message" : "Invalid Value"}, status = 400)
      
class DetailNotice(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    
    def get(self, request, *args, **kwargs):
        item = Notice.objects.get(pk=kwargs['pk'])
        item.notice_views += 1
        item.save()

        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        dt_now = datetime.datetime.now()
        item = Notice.objects.get(pk=kwargs['pk'])
        item.created_at = dt_now
        item.save()

        return super().put(request, *args, **kwargs)