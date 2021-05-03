import json
from django.contrib.auth.models import User
from django.http import response
from django.urls import reverse
# from rest_framework.authtoken import Token
from rest_framework.test import APITestCase
from rest_framework import status

from .models import *
from .serializers import *
twitter_account = '@17Ginono'

class GetTweetsTestCase(APITestCase):
    def test_get_tweet(self):
        response = self.client.get("/tweet-list")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AnalyseAccountTestCase(APITestCase):
    def test_analyse_account(self):
        data = {"username": twitter_account, "lang":"en"}
        response = self.client.post("/analysis-account", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        response = self.client.get(f"/gettwitter/{twitter_account}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["twitter_username"], twitter_account)

class AnalyseTextTestCase(APITestCase):
    def test_analyse_text(self):
        data = {"message":"@jnnybllstrs Dnt joke about these things, anak. Death & depression destroy lives, we shldnt wish for or joke about them. Let's hope fake news ito.", "lang":"en"}
        response = self.client.post("/analysis-text", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(round(response.data["result"]), 1)
