from rest_framework import serializers
from .models import Event, EventDetail, Favorite, Member, MemberAdmin, MemberUser, Notice

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'member_id',
            'member_pw',
            'member_name',
            'member_nickname',
            'member_auth',
        )
        model = Member

class MemberAdminSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'member_id',
            'member_admin_position',
        )
        model = MemberAdmin

class MemberUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'member_id',
            'member_user_birth',
            'member_user_phone',
            'member_user_email',
            'member_user_location',
            'member_user_num_of_family',
        )
        model = MemberUser

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'event_id',
            'member_id',
            'event_title',
            'event_location',
            'event_reporting_date',
            'event_views',
        )
        model = Event

class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'event_id',
            'event_management',
            'event_period_start',
            'event_period_end',
            'event_url',
            'event_image_url',
            'event_content',
        )
        model = EventDetail

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'favorite_id',
            'member_id',
            'event_id',
        )
        model = Favorite

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'notice_id', 
            'notice_title', 
            'member', 
            'notice_views', 
            'notice_reporting_date',
        )
        model = Notice

class NoticeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'notice_id', 
            'notice_title', 
            'notice_content', 
            'member', 
            'notice_views', 
            'notice_reporting_date',
        )
        model = Notice