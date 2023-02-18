from typing import List, Dict
import datetime


def eq_regions(r1: str, r2: str):
    return r1 == r2


def get_age(birthday: str):
    today = datetime.date.today()
    born = datetime.datetime.strptime(birthday, "%d.%m.%Y").date()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def match(user: dict, event: dict) -> bool:
    if not eq_regions(user['region'], event['region']):
        return False

    if not (event['ageFrom'] <= get_age(user['birthday']) <= event['ageTo']):
        return False

    # TODO: add ml functions
    return True


def classification_users_to_events(users: List[Dict], events: List[Dict]):
    result = []
    for user in users:
        for event in events:
            if match(user, event):
                pass

