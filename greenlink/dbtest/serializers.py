from rest_framework import serializers
from .models import Dbtest

class DbtestSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'content',
        )
        model = Dbtest