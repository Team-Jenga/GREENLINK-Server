from rest_framework import serializers
from .models import Main

class MainSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'content',
        )
        model = Main

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'member_id',
            'member_pw',
            'member_name',
            'member_nickname',
        )
        model = Main

class MemberAdminSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'member_id',
            'member_admin_position',
        )
        model = Main

class MemberUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'member_id',
            'member_user_birth',
            'member_user_phone',
            'member_user_email',
            'member_user_location',
            'member_user_number_of_family',
        )
        model = Main