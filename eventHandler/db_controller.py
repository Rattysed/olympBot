from eventHandler.models import Events, Subjects, User
import datetime
from typing import Union, List
from django.db.models import QuerySet
from .models import Events


def get_all_this_date(date) -> Union[QuerySet, List[Events]]:
    ev = Events.objects.filter(notify_date=date)
    return ev


def get_all_today() -> Union[QuerySet, List[Events]]:
    return get_all_this_date(datetime.date.today())


def create_new_user(grade: int, vk_id='', tg_id=''):
    if vk_id == tg_id == '':
        return AttributeError("Can't create user without any messenger account")
    user = User()
    user.vk_id = vk_id
    user.tg_id = tg_id
    user.grade = grade
    user.save()


def create_new_vk_user(id, grade):
    create_new_user(grade, vk_id=id)


def create_new_tg_user(id, grade):
    create_new_user(grade, tg_id=id)


if __name__ == '__main__':
    pass
    # print(get_all_this_date())
