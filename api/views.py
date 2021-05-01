from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import TweetSerializer
# Create your views here.


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Analyse': '/analyse/',
        'List': '/tweet-list/',
        'Get Tweet': '/get-tweet/<int:pk>',
        'Get Tweets By': '/get-tweet/<str:username>',
        'Save Tweet': '/tweet-save/'
    }
    return Response(api_urls)


@api_view(['GET'])
def tweetList(request):
    tweets = Tweets.objects.all()
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def tweetGet(request, pk):
    tweets = Tweets.objects.get(id=pk)
    serializer = TweetSerializer(tweets, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def tweetGetBy(request, username):
    tweets = Tweets.objects.filter(username=username)
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def tweetSave(request):

    serializer = TweetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
