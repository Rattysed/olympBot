import datetime
from typing import Union, List
from django.db.models import QuerySet
from .models import Event, User, Subject, Question
from eventHandler.vk_bot.vk_config import QUESTS


class CollectedData:
    subject_query: Union[QuerySet, List[Subject]] = None
    question_query: Union[QuerySet, List[Question]] = None
    subjects: List = []
    questions: List = []

    def update_data(self):
        self.subject_query = Subject.objects.all()
        self.question_query = Question.objects.all()
        self.subjects = list(self.subject_query)
        self.questions = list(self.question_query)


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


def get_user(vk_id='', tg_id=''):
    if vk_id == tg_id == '':
        raise ValueError("Can't find user without any messanger account")
    user = User.objects.get(vk_id=vk_id, tg_id=tg_id)
    return user


def get_user_question(vk_id):
    user = get_user(vk_id=vk_id)
    return str(user.current_question)


def get_user_chosen_subject(vk_id):
    user = get_user(vk_id=vk_id)
    return str(user.chosen_option)


def get_events_of_user(vk_id):
    events_of_user_sorted = dict()
    user = get_user(vk_id=vk_id)
    subjects = list(get_subjects())
    events = user.events.all()
    for sub in subjects:
        sub_events = events.filter(subject=sub)
        for ev in sub_events:
            if not events_of_user_sorted.get(sub.name, False):
                events_of_user_sorted[sub.name] = []
            events_of_user_sorted[sub.name].append(ev)
    return events_of_user_sorted


def generate_list(data):
    listed = []
    [listed.append(str(x)) for x in data]
    return listed


def is_user_in_database(tg_id='', vk_id=''):
    try:
        get_user(vk_id=vk_id, tg_id=tg_id)
        return True
    except:
        return False


def is_distribution(sender):
    user = get_user(sender)
    return user.is_rassylka


def change_user_grade(vk_id, grade):
    user = get_user(vk_id=vk_id)
    user.grade = grade
    user.save()


def change_user_question(vk_id, question):
    user = get_user(vk_id=vk_id)
    user.current_question = question
    user.save()


def change_user_events(vk_id, chosen_option: int):
    user = get_user(vk_id=vk_id)
    subject = user.chosen_option
    events = list(get_events_by_subject(subject))
    if chosen_option == 1:
        for ev in events:
            user.events.add(ev)
    elif chosen_option == 2:
        for ev in events:
            user.events.remove(ev)
    else:
        user.events.add(events[chosen_option - 3])
    print(events[0])


def change_user_chosen_subject(sender: str, subject_id: int):
    user = get_user(vk_id=sender)
    subject = DATA.subjects[subject_id - 1]
    user.chosen_option = subject
    user.save()


def turn_on_sending(vk_id):
    user = get_user(vk_id=vk_id)
    user.is_rassylka = 1
    user.save()


def turn_off_sending(vk_id):
    user = get_user(vk_id=vk_id)
    user.is_rassylka = 0
    user.save()


def create_new_vk_user(id, grade):
    create_new_user(grade, vk_id=id)


def create_new_tg_user(id, grade):
    create_new_user(grade, tg_id=id)


def create_new_user(grade: int, vk_id='', tg_id=''):
    if vk_id == tg_id == '':
        raise ValueError("Can't create user without any messenger account")
    user = User()
    user.vk_id = vk_id
    user.tg_id = tg_id
    user.grade = grade
    user.is_rassylka = 1
    user.current_question = DATA.questions[0]
    user.save()


def update_db():
    i = 1
    for q in QUESTS:
        values = {
            'short_name': q,
            'full_name': QUESTS[q],
        }
        Question.objects.update_or_create(id=i, defaults=values)
        i += 1
    print('ХУЙ')


if __name__ == '__main__':
    pass
    # print(get_subjects())
