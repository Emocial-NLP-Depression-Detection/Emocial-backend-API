from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass


class TwitterUser(models.Model):
    account = models.ForeignKey(User, on_delete=CASCADE, related_name="TwitterAcount", null=True, default=None)
    profile_name = models.CharField(max_length=50)
    twitter_username = models.CharField(max_length=15)
    profile = models.URLField(max_length=128, unique=True)

    def __str__(self):
        return f"Username: {self.twitter_username} Profile Name: {self.profile_name}"

class Tweets(models.Model):
    user = models.ForeignKey(TwitterUser, on_delete=CASCADE, related_name='tweeters', default=None)
    tweet = models.TextField(max_length=280, unique=True)
    prediction_value = models.FloatField()
    prediction_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.tweet} by {self.user.twitter_username} : {self.prediction_value}'


    