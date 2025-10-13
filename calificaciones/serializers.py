from rest_framework import serializers
from .models import CalificacionTributaria

class CalificacionTributariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalificacionTributaria
        fields = '__all__'
