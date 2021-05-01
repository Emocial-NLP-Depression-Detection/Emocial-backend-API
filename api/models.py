from django.db import models

# Create your models here.


class Tweets(models.Model):
    username = models.CharField(max_length=15)
    tweet = models.TextField(max_length=280)
    prediction_value = models.FloatField()
    prediction_date = models.DateTimeField()
    tweet_created_date = models.DateTimeField()

    def __str__(self):
        return f'{self.tweet} by {self.username} : {self.prediction_value}'
