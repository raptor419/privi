from rest_framework import serializers
from .models import *

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['content', 'options', 'max_time', 'correct_option']

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['title', 'content']

