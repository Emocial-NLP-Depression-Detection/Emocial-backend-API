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
    def test_analyse_english_account(self):
        data = {"username": twitter_account, "lang":"en"}
        response = self.client.post("/analysis-account", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        response = self.client.get(f"/gettwitter/{twitter_account}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["twitter_username"], twitter_account)
    
    def test_analyse_thai_account(self):
        data = {"username": "@prayutofficial", "lang":"th"}
        response = self.client.post("/analysis-account", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
        response = self.client.get(f"/gettwitter/@prayutofficial")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["twitter_username"], "@prayutofficial")

    def test_account_not_exit(self):
        data = {
                    "username" : "@Ginono17525", 
                    "lang":"en"
                }
        response = self.client.post("/analysis-account", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["messsage"], "Account not found")

class AnalyseTextTestCase(APITestCase):
    def test_analyse_english_text(self):
        data = {"message":"@jnnybllstrs Dnt joke about these things, anak. Death & depression destroy lives, we shldnt wish for or joke about them. Let's hope fake news ito.", "lang":"en"}
        response = self.client.post("/analysis-text", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(round(response.data["result"]), 1)
    def test_analyse_thai_text(self):
        data = {"message":"เครียดเรื่องฝึกงาน เครียดเรื่องครอบครัวที่เราต้องแบกรับทุกอย่าง มันโคตรแย่เลย", "lang":"th"}
        response = self.client.post("/analysis-text", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(round(response.data["result"]), 1)

class AuthenticationTestCase(APITestCase):
    
    def test_register(self):
        data = {
            "username" : "Gino",
            "email" : "ginono17@example.com",
            "password": "password",
            "twitterAcount": "@17Ginono",
            "status" : True
            }
        response = self.client.post("/register", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "Gino")

    
        data = {
                "username" : "Gino",
                "password": "password"
                }
        response = self.client.post("/login", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], response.cookies["token"].value)

        data = {
            "username" : "Gino",
            "email" : "ginono17@example.com",
            "password": "password",
            "twitterAcount": "@17Ginono",
            "status" : True
            }
        response = self.client.post("/register", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "User already logined")

        response = self.client.get("/get-logined")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "Gino")

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "success")