from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import *
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import *
from rest_framework.exceptions import AuthenticationFailed
from .serializers import TweetSerializer, TwitterUserSerializer, UserSerializer
# Create your views here.
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from . import utils


en_classifier = utils.DepressClassifier("en")
th_classifier = utils.DepressClassifier("th")

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Analyse': '/analyse/',
        'List': '/tweet-list/',
        'Get Tweet': '/get-tweet/<int:pk>',
        'Get Tweets By': '/get-tweets-by/<str:username>'
    }
    return Response(api_urls)


@api_view(['POST'])
def register(request):
    token = request.COOKIES.get("token")
    if token:
        raise AuthenticationFailed("User already logined")
    if TwitterUser.objects.filter(twitter_username=request.data['twitterAcount']).exists():
        data = request.data
        user = TwitterUser.objects.get(twitter_username=request.data['twitterAcount'])
        print(data)
        password = make_password(request.data["password"])
        user = User(username=request.data["username"], email=request.data["email"], password=password, twitterAcount=user, status=request.data["status"])
        if User.objects.filter(username=user.username).exists():
            return Response({"user_already_exit":True})
        else:
            
            user.save()
            serializer = UserSerializer(user)
            token = Token.objects.get(user=user).key
            data = serializer.data
            data["token"] = token
            return Response(data)
    else:
        twittercaller = utils.TweetCaller('en')
        twittercaller.callUser(request.data['twitterAcount'])
    
        profile_name = twittercaller.user.name
        profile_handle = twittercaller.twitterusername
        profile_pic = twittercaller.user.profile_image_url
        twitter_user = TwitterUser(profile_name=profile_name, twitter_username=profile_handle, profile=profile_pic)
        twitter_user.save()
        password = make_password(request.data["password"])
        user = User(username=request.data["username"], email=request.data["email"], password=password, twitterAcount=twitter_user, status=request.data["status"])
        if User.objects.filter(username=user.username).exists():
            return Response({"user_already_exit":True})
        else:
            user.save()
            serializer = UserSerializer(user)
            token = Token.objects.get(user=user).key
            data = serializer.data
            data["token"] = token
            return Response(data)
# {
# "username" : "Ginono17",
# "email" : "ginono17@example.com",
# "password": "password",
# "twitterAcount": "@17Ginono"
# }
@api_view(['POST'])
def login(request):
    username = request.data["username"]
    password = request.data["password"]

    user = User.objects.filter(username=username).first()
    if user is None:
        raise AuthenticationFailed("User not Found")
    
    if not user.check_password(password):
        raise AuthenticationFailed("Incorrect Password")
    token = Token.objects.get(user=user).key
    response = Response()
    response.set_cookie(key="token", value=token, httponly=True)
    response.data = {
        "token" : token
    }
    return response

# {
# "username":"Siravit",
# "password":"password"
# }

@api_view(['GET'])
def get_user(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def get_logined_user(request):
    token = request.COOKIES.get("token")
    if not token:
        raise AuthenticationFailed("Unauthenticated")
    
    
    user = Token.objects.get(key=token).user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def logout(request):
    token = request.COOKIES.get("token")
    if not token:
        raise AuthenticationFailed("Unauthenticated")
    response = Response()
    response.delete_cookie("token")
    response.data = {
        "message" : "success"
    }
    return response


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
    tweets =Tweets.objects.filter(user= TwitterUser.objects.filter(twitter_username=username).first())
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getuser(request, username):
    account =TwitterUser.objects.filter(twitter_username=username).first()
    serializer = TwitterUserSerializer(account, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def analysisAccount(request):
    if request.data['lang'] =="en":
        classifier = en_classifier
    else:
        classifier = th_classifier
    twittercaller = utils.TweetCaller(request.data['lang'])
    print(request.data)
    twittercaller.callUser(request.data['username'])
    if twittercaller.cannotFindUser:
        return Response({
            "messsage": "Account not found"
        })
    
    profile_name = twittercaller.user.name
    profile_handle = twittercaller.twitterusername
    profile_pic = twittercaller.user.profile_image_url
    if TwitterUser.objects.filter(twitter_username=profile_handle).exists():
        classifier.classify(twittercaller.savePost())
        for index, row in classifier.predictedData.iterrows():
            tweets = Tweets(user = TwitterUser.objects.filter(twitter_username=profile_handle).first(), tweet=row['Tweet'], prediction_value=row['Prediction'])
            tweets.save()
    else:    
        user = TwitterUser(profile_name=profile_name, twitter_username=profile_handle, profile=profile_pic)
        user.save()
        classifier.classify(twittercaller.savePost())
        for index, row in classifier.predictedData.iterrows():
            tweets = Tweets(user = user, tweet=row['Tweet'], prediction_value=row['Prediction'])
            
            tweets.save()

    tweets =Tweets.objects.filter(user= TwitterUser.objects.filter(twitter_username=request.data['username']).first())
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)
# {"username":"@17Ginono", "lang":"en"}

@api_view(['POST'])
def analyseText(request):
    if request.data['lang'] =="en":
        classifier = en_classifier
    else:
        classifier = th_classifier
    classifier.classifyText(request.data['message'])
    result = float(classifier.predict[0])
    prediction = {'message': request.data['message'],
                   'result': result}
    return Response(prediction)

# {"message":"@jnnybllstrs Dnt joke about these things, anak. Death & depression destroy lives, we shldnt wish for or joke about them. Let's hope fake news ito.", lang:"en"}