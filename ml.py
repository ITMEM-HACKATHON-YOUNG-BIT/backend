from typing import List, Dict
import datetime
from texts import *


def is_expiring(date: datetime.datetime):
    return (date - datetime.datetime.now()).days < 2


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
    for event in events:
        result.append({
            'message': EVENT_EXPIRED if is_expiring(event['registrationEndsAt']) else NEW_EVENT,
            'users': []
        })
        result[-1]['message'] = result[-1]['message'] % (event['name'],
                                                         event['organizerName'],
                                                         event['registrationBeginsAt'],
                                                         event['registrationEndsAt'],
                                                         event['beginsAt'],
                                                         event['endsAt'],
                                                         event['url'])
    for user in users:
        for index, event in enumerate(events):
            if match(user, event):
                result[index]['users'].append({
                    'first_name': user['first_name'],
                    'tgUserID': user['user_tg_id'],
                    'username': user['username_tg']
                })
    return result
