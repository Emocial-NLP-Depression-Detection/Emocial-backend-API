from django.db.models import fields
from api.models import Tweets
from rest_framework import serializers

from .models import *


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweets
        fields = '__all__'

class TwitterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterUser
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class QuestionaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionaire
        fields = "__all__"