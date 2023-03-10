import tempfile

import peewee
from fastapi import FastAPI, HTTPException, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from random import choice

from models import *
import utils
import ml
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
        username = body.username_tg.lower()
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
        user = db.Users.get(db.Users.username_tg == body.username.lower())
        user.user_tg_id = body.user_tg_id
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
                   "event_id": event.id,
                   "name": event.name,
                   "organizerName": event.organizerName,
                   "region": event.region,
                   "registrationBeginsAt": utils.to_datetime(event.registrationBeginsAt),
                   "registrationEndsAt": utils.to_datetime(event.registrationEndsAt),
                   "url": event.url,
                   "timestamp": utils.now(),
                   "minAmount": event.minAmount,
                   "maxAmount": event.maxAmount,
                   }
            db.Events.create(**req)
        except Exception as e:
            print(e)


@app_api.get('/events/get_by_delay')
def get_events(delay: int = 0):
    # resp = [
    #     {
    #         'message': 'text1',
    #         'users': [
    #             {'user_tg_id': 'id1', 'first_name': 'name1'}
    #         ]
    #     },
    #     ...
    # ]
    start_date = utils.now_delay(delay)
    try:
        events = list(db.Events.select().where(db.Events.timestamp >= start_date).dicts())
        if len(events) == 0:
            return []
    except Exception as e:
        print(e)
        return []

    try:
        users = list(db.Users.select().where(db.Users.user_tg_id.is_null(False)).dicts())
        if len(users) == 0:
            return []
    except Exception as e:
        print(e)
        return []

    return ml.classification_users_to_events(users, events)


def answer_question(body: UserMessage, from_site: bool):
    answer = ml.answer_question(body.message)
    username = None
    admin_chat = None

    if answer is None:
        try:
            username = db.Users.get(db.Users.user_tg_id == body.user_tg_id).username_tg
        except Exception as e:
            print(e)

        try:
            admin_chat = choice(list(db.Admins.select().dicts()))['admin_tg_id']
        except Exception as e:
            print(e)

    if answer is None and from_site:
        answer = "?????? ???????????? ???? ?????? ???????????? ?????????? ?????????? ????????????????????, ???????????????????????? ?????? ???? ????????????????????????????"

    return {'message': answer, 'username': username, 'admin_tg_id': admin_chat}


@app_api.get('/user/message')
def user_message(body: UserMessage):
    return answer_question(body, from_site=False)


@app_api.post('/user/message/site')
def user_message(body: UserMessage):
    return answer_question(body, from_site=True)


@app_api.get('/user/check_register')
def check_user_registered(user_site_id: int = -1):
    if user_site_id == -1:
        raise HTTPException(status_code=400)

    try:
        user = db.Users.get(db.Users.user_site_id == user_site_id)
        return user.user_tg_id is not None
    except:
        pass
    return False


@app_api.get('/user/message/voice')
async def create_file(file: bytes = File()):
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(file)
    f.close()
    return {"file_size": len(file)}
