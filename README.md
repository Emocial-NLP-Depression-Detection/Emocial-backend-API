# Emocial Backend API
Emocial Backend API is built for other emocial service to easily classify appearence trace of depression in text/string

## Install
```
virtualenv venv
```
```
pip install -r requirements.txt
```
Create .env file in root directory with content as follow
```
TWITTER_CONSUMER_KEY=
TWITTER_CONSUMER_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
DJANGO_SECRET=
```

```
python manage.py makemigrations
```
```
python manage.py migrate
```

## Running Server
```
python manage.py runserver
```
Server will start running on localhost at port 8000

## Creating super user to access database
```
python manage.py createsuperuser
```
Admin Console can be access at http://localhost:8000/admin

## REST API
the API example is described below

#### Get list of Tweets
Request
`GET /tweet-list/`
Response
```
HTTP 200 OK
Allow: GET, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "tweet": "@TheunderpaidO5 That is what you will be when I do the human instrumentality project. Or when I kill you and try to hide the evidence.",
        "prediction_value": 0.0,
        "prediction_date": "2021-05-02T09:05:59.431101Z",
        "user": 1
    },
    {
        "id": 2,
        "tweet": "Welp, when day breaks was fake all along.\n*Immedieatly dies after tweet*",
        "prediction_value": 0.0,
        "prediction_date": "2021-05-02T09:05:59.522200Z",
        "user": 1
    },
    {
        "id": 3,
        "tweet": "SmallAnt is the best streamer. Man made a whole pokemon chalenge run youtube video in 17 hours.",
        "prediction_value": 0.0,
        "prediction_date": "2021-05-02T09:05:59.605766Z",
        "user": 1
    },
]
```
### Get Tweets by ID
Request
`GET /get-tweet/<int:pk>`
Response
```
HTTP 200 OK
Allow: GET, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "tweet": "@TheunderpaidO5 That is what you will be when I do the human instrumentality project. Or when I kill you and try to hide the evidence.",
    "prediction_value": 0.0,
    "prediction_date": "2021-05-02T09:05:59.431101Z",
    "user": 1
}
```

### Get All Tweets Of Someone
Request
`GET /get-tweets-by/<str:username>`
Response
```
HTTP 200 OK
Allow: OPTIONS, GET
Content-Type: application/json
Vary: Accept

[
    {
        "id": 1,
        "tweet": "@TheunderpaidO5 That is what you will be when I do the human instrumentality project. Or when I kill you and try to hide the evidence.",
        "prediction_value": 0.0,
        "prediction_date": "2021-05-02T09:05:59.431101Z",
        "user": 1
    },
    {
        "id": 2,
        "tweet": "Welp, when day breaks was fake all along.\n*Immedieatly dies after tweet*",
        "prediction_value": 0.0,
        "prediction_date": "2021-05-02T09:05:59.522200Z",
        "user": 1
    },
]
```

### Get All Twitter Account Of Someone
Request
`GET gettwitter/<str:username>`
Response
```
HTTP 200 OK
Allow: OPTIONS, GET
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "profile_name": "Ginono 17",
    "twitter_username": "@17Ginono",
    "profile": "http://pbs.twimg.com/profile_images/1368740815044931584/b04Es4_v_normal.jpg",
    "account": null
}
```


### Analyse Someone's Twitter account
#### Notice: If the Twitter account has never been encounter before the account will got saved to the database
The lang parameter signifies both which language of the tweets to be imported and which neural network to use 
Request
`POST /analysis-account/`
```
{
    "username" : "@Ginono17", 
    "lang":"en"
}
```

Response
```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

[
    {
        "id": 461,
        "tweet": "Wow",
        "prediction_value": 0.0,
        "prediction_date": "2021-05-02T09:45:22.929100Z",
        "user": 3
    },
    {
        "id": 462,
        "tweet": "Girl you have a sweet pussy",
        "prediction_value": 0.0,
        "prediction_date": "2021-05-02T09:45:23.001097Z",
        "user": 3
    },
    {
        "id": 463,
        "tweet": "Hi i like yur pussy",
        "prediction_value": 0.0,
        "prediction_date": "2021-05-02T09:45:23.086098Z",
        "user": 3
    }
]
```

If account not found will will return message saying account not found
```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "messsage": "Account not found"
}

```
### Analyse Text
#### Notice: Result will not get saved to database
Request
`POST /analysis-text/`
```
{
    "message":"@jnnybllstrs Dnt joke about these things, anak. Death & depression destroy lives, we shldnt wish for or joke about them. Let's hope fake news ito.", "lang":"en"
}
```

Response
```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "message": "@jnnybllstrs Dnt joke about these things, anak. Death & depression destroy lives, we shldnt wish for or joke about them. Let's hope fake news ito.",
    "result": 0.999992847442627
}
```


### Register an account
#### Notice: password will automaticly got hashed
#### status: True is doctor and False is Patient
Request
`POST /register/`
```
{
 "username" : "Gino",
 "email" : "ginono17@example.com",
 "password": "password",
 "twitterAcount": "@17Ginono",
 "status" : True
 }
```

Response
```
HTTP 200 OK
Allow: OPTIONS, POST
Content-Type: application/json
Vary: Accept

{
    "id": 5,
    "last_login": null,
    "is_superuser": false,
    "first_name": "",
    "last_name": "",
    "is_staff": false,
    "is_active": true,
    "date_joined": "2021-05-04T14:24:07.067879Z",
    "username": "Gino",
    "email": "ginono17@example.com",
    "password": "pbkdf2_sha256$260000$wxvukj70d17I1gf08U9sJf$g2zBwUINBGDyCIbrYsRcnsJh2hBBIGdaBPP2FG2kBK0=",
    "twitterAcount": 1,
    "groups": [],
    "user_permissions": []
}
```

### Get User by ID
Request
`GET /get-user/<int:pk>`
Response
```
HTTP 200 OK
Allow: OPTIONS, GET
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "last_login": "2021-05-02T14:49:09.701661Z",
    "is_superuser": true,
    "first_name": "",
    "last_name": "",
    "is_staff": true,
    "is_active": true,
    "date_joined": "2021-05-02T12:00:10.570253Z",
    "username": "root",
    "email": "",
    "password": "pbkdf2_sha256$260000$bqmbyezILn7ZIjanRCzfK8$YY9dbLAh0I3WjrKAI/2DvGqWitpneGC+Dwkk1wroDSI=",
    "status": false,
    "twitterAcount": null,
    "groups": [],
    "user_permissions": []
}
```


### login to an account
#### Notice: Token will automatically saved as cookie for later use
`POST /login/`
```
{
 "username" : "Siravit",
 "password": "password"
 }
```

Response
```
HTTP 200 OK
Allow: OPTIONS, POST
Content-Type: application/json
Vary: Accept

{
    "token": "34166817967327076e79e5bfa6cfdd6c08096cc6"
}
```

### Get logined user
#### if the user is not login will raise a error message
Request
`GET /get-logined`
Response
```
HTTP 200 OK
Allow: OPTIONS, GET
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "last_login": "2021-05-02T14:49:09.701661Z",
    "is_superuser": true,
    "first_name": "",
    "last_name": "",
    "is_staff": true,
    "is_active": true,
    "date_joined": "2021-05-02T12:00:10.570253Z",
    "username": "root",
    "email": "",
    "password": "pbkdf2_sha256$260000$bqmbyezILn7ZIjanRCzfK8$YY9dbLAh0I3WjrKAI/2DvGqWitpneGC+Dwkk1wroDSI=",
    "status": false,
    "twitterAcount": null,
    "groups": [],
    "user_permissions": []
}
```

### Log user out
### Notice: Cookie will get delete as soon as this URL is fetch
Request
`GET /logout`
Response
```
HTTP 200 OK
Allow: OPTIONS, GET
Content-Type: application/json
Vary: Accept

{
    "message": "success"
}
```

### Analyse Questionaire
#### Notice: If the user is logged in result will automatically saved to database
`POST /analyse-question/`
```
{
    "q1": "man", 
    "q2":"woman", 
    "lang":"en"
}
```

Response
```
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "q1": "man",
    "prediction1": 2.3708851415449317e-07,
    "q2": "woman",
    "prediction2": 2.2717343028944015e-07,
    "mean": 2.3213097222196666e-07,
    "user": 8
}
```