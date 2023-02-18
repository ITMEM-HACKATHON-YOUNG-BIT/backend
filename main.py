import peewee
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

from models import *
import utils
import db

app_api = FastAPI()
logger = logging.getLogger(__name__)

origins = ["*"]

app_api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app_api.get('/')
def home():
    return {'Hello': 'world'}
    # return JSONResponse(content={'Hello': 'world'}, headers=headers, status_code=200)


@app_api.post('/user/create/site')
def new_user_site(body: NewUserSite):
    try:
        db.Users.create(first_name=body.first_name,
                        second_name=body.second_name,
                        third_name=body.third_name,
                        user_site_id=body.user_site_id,
                        birthday=body.birthday,
                        sex=body.sex,
                        phone=body.phone,
                        email=body.email,
                        region=body.region)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@app_api.post('/user/set/tg_id')
def set_tg_id(body: SetTgId):
    print(body)
    try:
        username = body.username_tg
        if not username.startswith('@'):
            username = '@' + username
        q = db.Users.update(username_tg=username).where(db.Users.user_site_id == body.user_site_id)
        count = q.execute()
        if count == 0:
            raise HTTPException(status_code=400, detail=f'no such user with id == {body.user_site_id}')
    except HTTPException as he:
        raise he
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@app_api.post('/user/create/tg')
def new_user_tg(body: NewUserTg):
    try:
        # db.Users.update(user_tg_id=body.tgUserID).where(username_tg=body.username)
        user = db.Users.get(db.Users.username_tg == body.username)
        user.user_tg_id = body.tgUserID
        resp = {'first_name': user.first_name, 'second_name': user.second_name}
        user.save()
        return resp
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@app_api.post('/postEvent')
def add_events(body: NewEvents):
    for event in body.items:
        try:
            req = {"ageFrom": event.ageFrom,
                   "ageTo": event.ageTo,
                   "beginsAt": utils.to_datetime(event.beginsAt),
                   "endsAt": utils.to_datetime(event.endsAt),
                   "eventType": event.eventType,
                   "event_id": '',
                   "name": event.name,
                   "organizerName": event.organizerName,
                   "region": event.region,
                   "registrationBeginsAt": utils.to_datetime(event.registrationBeginsAt),
                   "registrationEndsAt": utils.to_datetime(event.registrationEndsAt),
                   "url": event.url,
                   "timestamp": utils.now()
                   }
            db.Events.create(**req)
        except Exception as e:
            print(e)


@app_api.get('/events/get_by_delay')
def get_events(delay: int = 0):
    resp = [
        # {
        #     'message': 'text1',
        #     'users': [
        #         {'user_tg_id': 'id1', 'first_name': 'name1'}
        #     ]
        # },
        # ...
    ]
    start_date = utils.now_delay(delay)
    try:
        events = list(db.Events.select().where(db.Events.timestamp >= start_date).dicts())
        if len(events) == 0:
            return []
    except Exception as e:
        print(e)
        return []

    try:
        users = list(db.Users.select().where(db.Users.user_tg_id.is_null(False)))
        if len(users) == 0:
            return []
    except Exception as e:
        print(e)


