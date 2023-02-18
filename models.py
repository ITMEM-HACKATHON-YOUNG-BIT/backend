from pydantic import BaseModel
from typing import List, Optional


class NewUserTg(BaseModel):
    user_tg_id: int
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
    id: str
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
    minAmount: Optional[int]
    maxAmount: Optional[int]


class NewEvents(BaseModel):
    items: List[Event]


class UserMessage(BaseModel):
    user_tg_id: int
    message: str
