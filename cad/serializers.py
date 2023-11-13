from rest_framework import serializers
from .models import *

class CadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cad
        fields = '__all__'
        read_only_fields = ('_id',)
