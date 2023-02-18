from pydantic import BaseModel
from typing import List


class NewUserTg(BaseModel):
    tgUserID: int
    username: str


class NewUserSite(BaseModel):
    user_site_id: int
    first_name: str
    second_name: str
    third_name: str
    birthday: str
    sex: str
    phone: str
    email: str
    region: str


class SetTgId(BaseModel):
    user_site_id: int
    username_tg: str


class GetCards(BaseModel):
    user_token: str


class Event(BaseModel):
    id: int
    name: str
    organizerName: str
    region: str
    eventType: str
    ageFrom: int
    ageTo: int
    beginsAt: str
    endsAt: str
    registrationBeginsAt: str
    registrationEndsAt: str
    url: str


class NewEvents(BaseModel):
    items: List[Event]
