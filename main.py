from fastapi import FastAPI

from pydantic import BaseModel
from typing import List


class SetCategories(BaseModel):
    user_token: str
    categories: List[str]


class GetCards(BaseModel):
    user_token: str


app_api = FastAPI()


@app_api.get('/')
def home():
    return {'Hello': 'world'}


# @app_api.post('/api/set_categories')
# def new_user(body: SetCategories):
#     return users.set_categories(body.user_token, body.categories)
#
#
# @app_api.get('/api/get_cards')
# def cards(user_token: str):
#     return recsys.generate_first_cards(user_token)


# @app.get('/test/...blabla...')
# def handle_testFunc(...args...):
#     return testFunc(...args...)

# recsys.generate_first_cards('', [])