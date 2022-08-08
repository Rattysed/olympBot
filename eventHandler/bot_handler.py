from .db_controller import get_all_today
from eventHandler.vk_bot.vk_functions import *


def make_distribution():
    events = get_all_today()
    print(len(events))
    for event in events:
        users = event.user_set.all()
        tg_users = set()
        vk_users = set()
        for user in users:
            tg_users.add(user.tg_id)
            vk_users.add(user.vk_id)
        message = f"""Олимпиада {event.name} для {str(event.event_grade)} класса
по предметам {' '.join([x['name'] for x in event.subject.all().values('name')])} (профили:{' '.join([x['name'] for x in event.profile.all().values('name')])})
Сроки проведения: {event.period}
Уровень олимпиады: {event.level}
Ссылка на сайт олимпиады: {event.event_url}
Дополнительная информация: {event.description}"""
#         huynya(vk_users, message)
