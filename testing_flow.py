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
            {'id': 'c490a68f-9354-40b0-8f81-61978d48ccff', 'name': 'Конкурс молодежных проектов «Есть идея!» 2023',
             'organizerName': 'Министерство внутренней, информационной и молодежной политики Магаданской области',
             'region': 'Магаданская область', 'eventType': 'Региональный', 'ageFrom': 14, 'ageTo': 35,
             'beginsAt': '2023-01-31 00:00:00', 'endsAt': '2023-03-01 23:59:00',
             'registrationBeginsAt': '2023-01-31 00:00:00', 'registrationEndsAt': '2023-03-01 23:59:59',
             'url': 'https://grants.myrosmol.ru/events/c490a68f-9354-40b0-8f81-61978d48ccff', 'maxAmount': 150000,
             'minAmount': 10000},
            {'id': '354f80bc-c6ac-4112-92aa-9aacf1cf0db1', 'name': 'Сезон образовательных мероприятий "Грантовый сок"',
             'organizerName': 'АНО «ДОМ МОЛОДЕЖИ»', 'region': 'Крым республика', 'eventType': 'Региональный',
             'ageFrom': 14, 'ageTo': 35, 'beginsAt': '2023-02-06 09:00:00', 'endsAt': '2023-04-16 22:00:00',
             'registrationBeginsAt': '2023-02-06 22:00:00', 'registrationEndsAt': '2023-04-16 22:00:00',
             'url': 'https://grants.myrosmol.ru/events/354f80bc-c6ac-4112-92aa-9aacf1cf0db1', 'maxAmount': None,
             'minAmount': None},
            {'id': 'ea3c1713-9bea-4dbe-93e4-67a08a822aa2',
             'name': 'Республиканский конкурс социальной рекламы антинаркотической направленности и пропаганды здорового образа жизни«Мы – за здоровое будущее»',
             'organizerName': 'Агентство по делам молодежи Республики Калмыкия, Бюджетное учреждение Республики Калмыкия «Республиканский центр молодежи»',
             'region': 'Калмыкия республика', 'eventType': 'Региональный', 'ageFrom': 14,
             'ageTo': 35, 'beginsAt': '2023-02-16 00:00:00', 'endsAt': '2023-03-30 00:00:00',
             'registrationBeginsAt': '2023-02-16 00:00:00',
             'registrationEndsAt': '2023-03-16 14:00:00',
             'url': 'https://grants.myrosmol.ru/events/ea3c1713-9bea-4dbe-93e4-67a08a822aa2',
             'maxAmount': None, 'minAmount': None},
            {'id': '7a7a8f38-d8ad-4b37-b771-cba91765127b', 'name': 'Акселерационная программа "СТАРТ"',
             'organizerName': 'ГАУ "Агентство развития общественных проектов и инициатив Кузбасса"',
             'region': 'Кемеровская область', 'eventType': 'Региональный', 'ageFrom': 14, 'ageTo': 35,
             'beginsAt': '2023-02-20 00:00:00', 'endsAt': '2023-03-31 00:00:00',
             'registrationBeginsAt': '2023-02-16 08:00:00', 'registrationEndsAt': '2023-03-31 23:59:00',
             'url': 'https://grants.myrosmol.ru/events/7a7a8f38-d8ad-4b37-b771-cba91765127b', 'maxAmount': None,
             'minAmount': None},
            {'id': 'e94b384a-6496-4590-a711-afc0f6df4bfd', 'name': 'Внимание! инфлюенсеры проектной деятельности',
             'organizerName': 'Чаунина Инесса', 'region': 'Донецкая Народная Республика', 'eventType': 'Всероссийский',
             'ageFrom': 18, 'ageTo': 35, 'beginsAt': '2023-03-20 00:00:00', 'endsAt': '2023-03-30 00:00:00',
             'registrationBeginsAt': '2023-02-14 00:00:00', 'registrationEndsAt': '2023-03-28 00:00:00',
             'url': 'https://grants.myrosmol.ru/events/e94b384a-6496-4590-a711-afc0f6df4bfd', 'maxAmount': None,
             'minAmount': None},
            {'id': '0c98845d-1d42-4f8c-a3cf-717293803445',
             'name': 'Конкурс молодежных инициатив Кунгурского муниципального округа Пермского края',
             'organizerName': 'Управление молодежной политики и туризма администрации Кунгурского муниципального округа Пермского края',
             'region': 'Пермский край', 'eventType': 'Муниципальный', 'ageFrom': 14, 'ageTo': 35,
             'beginsAt': '2023-03-20 10:00:00', 'endsAt': '2023-03-20 10:00:00',
             'registrationBeginsAt': '2023-01-31 08:00:00',
             'registrationEndsAt': '2023-03-15 21:59:00',
             'url': 'https://grants.myrosmol.ru/events/0c98845d-1d42-4f8c-a3cf-717293803445',
             'maxAmount': 100000, 'minAmount': None}]
    })


create_user()
set_tg()
reg_tg()
add_events()
