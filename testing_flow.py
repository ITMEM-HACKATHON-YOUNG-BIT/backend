import requests


def create_user():
    requests.post(url='http://localhost:8000/user/create/site', json={
      "user_site_id": 10,
      "first_name": "илья",
      "second_name": "пономаренко",
      "third_name": "сергеевич",
      "birthday": "13.04.2003",
      "sex": "муж",
      "phone": "+79235377711",
      "email": "ponomarenko@niuitmo.ru",
      "region": "г. Юрга"
    })


def set_tg():
    requests.post(url='http://localhost:8000/user/set/tg_id', json={
      "user_site_id": 10,
      "username_tg": "@noisegain"
    })


def reg_tg():
    requests.post(url='http://localhost:8000/user/create/tg', json={
      "user_tg_id": 12345,
      "username": "@noisegain"
    })


def add_events():
    requests.post(url='http://localhost:8000/postEvent', json={
        "items": [
            {
                "id": "c490a68f-9354-40b0-8f81-61978d48ccff",
                "name": "Конкурс молодежных проектов «Есть идея!» 2023",
                "organizerName": "Министерство внутренней, информационной и молодежной политики Магаданской области",
                "region": "Магаданская область",
                "eventType": "Региональный",
                "ageFrom": 14,
                "ageTo": 35,
                "beginsAt": "2023-01-31 00:00:00",
                "endsAt": "2023-03-01 23:59:00",
                "registrationBeginsAt": "2023-01-31 00:00:00",
                "registrationEndsAt": "2023-03-01 23:59:59",
                "url": "https://grants.myrosmol.ru/events/c490a68f-9354-40b0-8f81-61978d48ccff",
                'maxAmount': 1000000,
                'minAmount': None
                },
            {
                "id": "kjer094f-9354-40b0-8f81-61978d48ccaa",
                "name": "Молодежный бит",
                "organizerName": "Министерство внутренней, информационной и молодежной политики СПб",
                "region": "Ленинградская область",
                "eventType": "Региональный",
                "ageFrom": 15,
                "ageTo": 20,
                "beginsAt": "2023-01-31 00:00:00",
                "endsAt": "2023-03-01 23:59:00",
                "registrationBeginsAt": "2023-01-31 00:00:00",
                "registrationEndsAt": "2023-03-01 23:59:59",
                "url": "https://grants.myrosmol.ru/events/event1",
                'maxAmount': 100000,
                'minAmount': None
                }
        ]
    })


# create_user()
# set_tg()
# reg_tg()
add_events()
