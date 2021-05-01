from django.urls import path

from . import views

urlpatterns = [
    path("", views.apiOverview, name="api-overview"),
    path("tweet-list", views.tweetList, name="tweet-list"),
    path("get-tweet/<int:pk>", views.tweetGet, name="get-tweet"),
    path("get-tweets-by/<str:username>", views.tweetGetBy, name="get-tweets-by"),
    path("tweet-save", views.tweetSave, name="tweet-save"),
]
