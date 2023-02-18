import peewee
from fastapi import FastAPI, HTTPException
import logging

from models import *
import db


app_api = FastAPI()
logger = logging.getLogger(__name__)


@app_api.get('/')
def home():
    return {'Hello': 'world'}


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


# def
