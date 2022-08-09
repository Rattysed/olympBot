import datetime
from typing import Union, List
from django.db.models import QuerySet
from .models import Event, User, Subject, Question


class CollectedData:
    subject_query: Union[QuerySet, List[Subject]] = None
    event_query: Union[QuerySet, List[Event]] = None
    question_query: Union[QuerySet, List[Question]] = None
    user_query: Union[QuerySet, List[User]] = None
    subjects: List = []
    events: List = []
    questions: List = []
    users: List = []

    def update_data(self):
        self.event_query = Event.objects.all()
        self.subject_query = Subject.objects.all()
        self.question_query = Question.objects.all()
        self.user_query = User.objects.all()
        self.subjects = list(self.subject_query)
        self.events = list(self.event_query)
        self.questions = list(self.question_query)
        self.users = list(self.user_query)


DATA = CollectedData()
DATA.update_data()


def get_all_this_date(date) -> Union[QuerySet, List[Event]]:
    ev = Event.objects.filter(notify_date=date)
    return ev


def get_all_today() -> Union[QuerySet, List[Event]]:
    return get_all_this_date(datetime.date.today())


def get_subjects() -> Union[QuerySet, List[Event]]:
    sub = Subject.objects.all()
    return sub


def get_events_by_subject(subject) -> Union[QuerySet, List[Event]]:
    events = Event.objects.filter(subject=subject)
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
    user.is_rassylka = 0
    user.current_question = DATA.questions[0]
    user.save()


def get_user(vk_id='', tg_id=''):
    if vk_id == tg_id == '':
        raise ValueError("Can't find user without any messanger account")
    user = User.objects.get(vk_id=vk_id, tg_id=tg_id)
    return user


def get_user_question(vk_id):
    user = get_user(vk_id=vk_id)
    return str(user.current_question)


def change_user_grade(vk_id, grade):
    user = get_user(vk_id=vk_id)
    user.grade = grade
    user.save()


def change_user_question(vk_id, question):
    user = get_user(vk_id=vk_id)
    user.current_question = question
    user.save()


def add_events_by_subject(subject: Subject, user: User):
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
