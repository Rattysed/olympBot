from eventHandler.models import Events, Subjects, User
import datetime
from typing import Union, List
from django.db.models import QuerySet
from .models import Events, User, Subjects


def get_all_this_date(date) -> Union[QuerySet, List[Events]]:
    ev = Events.objects.filter(notify_date=date)
    return ev


def get_all_today() -> Union[QuerySet, List[Events]]:
    return get_all_this_date(datetime.date.today())


def get_subjects() -> Union[QuerySet, List[Events]]:
    sub = Subjects.objects.filter()
    return sub


def get_events_for_this_subject(subject) -> Union[QuerySet, List[Events]]:
    output = Events.objects.filter(subject=subject)
    return output


def is_user_in_database(tg_id='', vk_id=''):
    if tg_id == vk_id == '':
        raise ValueError
    elif tg_id == '':
        user = User.objects.filter(vk_id=vk_id)
    elif vk_id == '':
        user = User.objects.filter(tg_id=tg_id)
    if len(list(user)) >= 1:
        return True
    else:
        return False


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
    # print(get_subjects())
