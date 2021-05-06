from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from . import utils
urlpatterns = [
    path("", views.apiOverview, name="api-overview"),
    path("tweet-list", views.tweetList, name="tweet-list"),
    path("get-tweet/<int:pk>", views.tweetGet, name="get-tweet"),
    path("get-tweets-by/<str:username>", views.tweetGetBy, name="get-tweets-by"),
    path("analysis-account", views.analysisAccount, name="analysis-account"),
    path("gettwitter/<str:username>", views.getuser, name="get-twitter"),
    path("analysis-text", views.analyseText, name="analysis-text"),
    path("register", views.register, name="register"),
    path("get-user/<int:pk>", views.get_user, name="get-user"),
    path("login", views.login, name="login"),
    path("get-logined", views.get_logined_user, name="get-logined-user"),
    path("logout", views.logout, name="logout")
]

en_classifier = utils.DepressClassifier("en")
th_classifier = utils.DepressClassifier("th")