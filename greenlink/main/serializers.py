from rest_framework import serializers
from .models import Event, Favorite, Member, MemberAdmin, MemberUser, Notice

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
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
            'member',
            'event_title',
            'event_location',
            'event_reporting_date',
            'event_views',
            'event_management',
            'event_period_start', 
            'event_period_end',
            'event_url',
            'event_image_url',
            'event_content'
        )
        model = Event

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'member',
            'event',
        )
        model = Favorite

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 
            'notice_title', 
            'notice_content', 
            'member', 
            'created_at',
            'notice_views',
        )
        model = Notice