# Emocial Backend API
Emocial Backend API is built for other emocial service to easily classify appearence trace of depression in text/string

## Install
```
virtualenv venv
```
```
pip install -r requirements.txt
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
Request
`POST /analyse/`
```
{
    "username" : "@Ginono17"
}
```
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