from eventHandler.models import Events, Subjects, User
import datetime
from typing import Union, List
from django.db.models import QuerySet
from .models import Events, User, Subjects


class CollectedData:
    subject_query: Union[QuerySet, List[Subjects]] = None
    event_query: Union[QuerySet, List[Events]] = None
    subjects: List = []
    events: List = []

    def update_data(self):
        self.event_query = Events.objects.all()
        self.subject_query = Subjects.objects.all()
        self.subjects = list(self.subject_query)
        self.events = list(self.event_query)


DATA = CollectedData()
DATA.update_data()


def get_all_this_date(date) -> Union[QuerySet, List[Events]]:
    ev = Events.objects.filter(notify_date=date)
    return ev


def get_all_today() -> Union[QuerySet, List[Events]]:
    return get_all_this_date(datetime.date.today())


def get_subjects() -> Union[QuerySet, List[Events]]:
    sub = Subjects.objects.all()
    return sub


def get_events_by_subject(subject) -> Union[QuerySet, List[Events]]:
    events = Events.objects.filter(subject=subject)
    return events


def is_user_in_database(tg_id='', vk_id=''):
    try:
        get_user(vk_id=vk_id, tg_id=tg_id)
        return True
    except:
        return False


def create_new_user(grade: int, vk_id='', tg_id=''):
    if vk_id == tg_id == '':
        raise ValueError("Can't create user without any messenger account")
    user = User()
    user.vk_id = vk_id
    user.tg_id = tg_id
    user.grade = grade
    user.save()


def get_user(vk_id='', tg_id=''):
    if vk_id == tg_id == '':
        raise ValueError("Can't find user without any messanger account")
    user = User.objects.get(vk_id=vk_id, tg_id=tg_id)
    return user


def add_events_by_subject(subject: Subjects, user: User):
    events = get_events_by_subject(subject)
    for ev in events:
        user.events.add(ev)


def create_new_vk_user(id, grade):
    create_new_user(grade, vk_id=id)


def create_new_tg_user(id, grade):
    create_new_user(grade, tg_id=id)


if __name__ == '__main__':
    pass
    # print(get_subjects())
