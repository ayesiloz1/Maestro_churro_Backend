from rest_framework import serializers
from .models import Churro
from .models import Survey

class ChurroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Churro
        fields = ['id', 'name', 'description', 'price', 'imageUrl']

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'experience', 'feedback']