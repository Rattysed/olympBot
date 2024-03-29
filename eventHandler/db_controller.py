import datetime
from typing import Union, List
from django.db.models import QuerySet
from .models import *
from eventHandler.vk_bot.vk_config import *


class CollectedData:
    subject_query: Union[QuerySet, List[Subject]] = None
    question_query: Union[QuerySet, List[Question]] = None
    profile_query: Union[QuerySet, List[Question]] = None
    subjects: List = []
    questions: List = []
    profiles: List = []

    def update_data(self):
        self.subject_query = Subject.objects.all()
        self.question_query = Question.objects.all()
        self.profile_query = Question.objects.all()
        self.subjects = list(self.subject_query)
        self.questions = list(self.question_query)
        self.profiles = list(self.question_query)


DATA = CollectedData()
DATA.update_data()


def drop_events_of_user(vk_id):
    user = get_user(vk_id=vk_id)
    user.events.clear()
    user.save()


def get_all_this_date(date) -> Union[QuerySet, List[RawEvent]]:
    ev = Event.objects.filter(notify_date=date).values('raw_event')
    # ev = RawEvent.objects.filter(notify_date=date)
    return ev


def get_all_this_grade_today(grade):
    evs_by_grade = set()
    events = get_all_today()
    for sub in events:
        print(sub.grade)
        if sub.grade == grade:
            evs_by_grade.add(sub)
    return evs_by_grade


def get_all_today() -> Union[QuerySet, List[Event]]:
    return get_all_this_date(datetime.date.today())


def get_subjects() -> Union[QuerySet, List[Event]]:
    sub = Subject.objects.all()
    return sub


def get_events_by_subject(subject) -> Union[QuerySet, List[Event]]:
    events = RawEvent.objects.filter(subject=subject)
    return events


def get_events_by_subject_and_grade(vk_id, subject) -> Union[QuerySet, List[Event]]:
    user = get_user(vk_id=vk_id)
    events = RawEvent.objects.filter(subject=subject, min_grade__gte=user.grade, max_grade__lte=user.grade,
                                     is_finished=False)
    # for subev in subevents:
    #     print(subev.name)  <----- это получение нормального названия саб ивента
    return events


def get_user(vk_id='', tg_id=''):
    if vk_id == tg_id == '':
        raise ValueError("Can't find user without any messanger account")
    user = User.objects.get(vk_id=vk_id, tg_id=tg_id)
    return user


def get_user_question(vk_id):
    user = get_user(vk_id=vk_id)
    return user.current_question


def get_user_chosen_subject(vk_id):
    user = get_user(vk_id=vk_id)
    return user.chosen_option


def get_main_events_of_user(vk_id):
    user = get_user(vk_id=vk_id)
    mains = []
    events = user.events.all()
    for ev in events:
        all_mains = ev.event_set.all()
        for main in all_mains:
            mains.append(main)
    print(mains)
    return mains


def get_events_of_user(vk_id):
    events_of_user_sorted = dict()
    user = get_user(vk_id=vk_id)
    subjects = list(get_subjects())
    for sub in subjects:
        events = get_events_by_subject_and_grade(vk_id, sub)
        for ev in events:

            if ev in user.events.all():
                if not events_of_user_sorted.get(sub.name, False):
                    events_of_user_sorted[sub.name] = []
                events_of_user_sorted[sub.name].append(ev)
    return events_of_user_sorted


def get_current_rollback(sender):  # получение нужного словаря в списке COMMAND_ROLLBACK для кнопки "назад"
    return list(filter(lambda item: item['current_question'] == str(get_user_question(sender)), COMMAND_ROLLBACK))


def get_rollback_question(sender):
    rollback_quest = get_current_rollback(sender)[0].get('rollback_question', False)
    return rollback_quest


def generate_list(data):
    return [str(x) for x in data]


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


def change_user_question(vk_id, question, **kwargs):
    user = get_user(vk_id=vk_id)
    flag = kwargs.get('is_string', False)
    if flag:
        user.current_question = Question.objects.get(short_name=str(question))
    else:
        user.current_question = question
    user.save()


def change_user_events(vk_id, chosen_option: int):
    user = get_user(vk_id=vk_id)
    subject = user.chosen_option
    events = list(get_events_by_subject_and_grade(vk_id, subject))
    if chosen_option == 1:
        for ev in events:
            user.events.add(ev)
    elif chosen_option == 2:
        for ev in events:
            user.events.remove(ev)
    else:
        events_of_user = get_events_of_user(vk_id).get(str(subject), [])
        formatted_events_of_user = set()
        for el in events_of_user:
            formatted_events_of_user.add(str(el))
        print(formatted_events_of_user)

        if str(events[chosen_option - 3]) not in formatted_events_of_user:
            user.events.add(events[chosen_option - 3])
        else:
            user.events.remove(events[chosen_option - 3])
    user.save()


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


def remove_user_events(vk_id, chosen_option: int):
    user = get_user(vk_id=vk_id)
    subject = user.chosen_option
    events = list(get_events_by_subject(subject))
    user.events.remove(events[chosen_option - 1])
    user.save()


def set_up_next_event(event: Event):
    return
    if event.next_event_id is None:
        return
    sub_events = event.subevent_set.all()
    grade_to_event = dict()
    for ev in sub_events:
        grade_to_event[ev.grade] = ev
    next_event = event.next_event_id
    next_sub_events = next_event.subevent_set.all()
    for ev in next_sub_events:
        last_ev = grade_to_event.get(ev.grade, None)
        if last_ev is None:
            continue  # TODO: Придумать, что делать, когда нет нужного эвента под класс
        for user in last_ev.user_set.all():
            ev.user_set.add(user)
    event.is_visible = False
    next_event.is_visible = True
    event.save()
    next_event.save()


def setup_db():
    for i, q in enumerate(QUESTS):
        values = {
            'short_name': q,
            'full_name': QUESTS[q],
        }
        Question.objects.update_or_create(id=i + 1, defaults=values)
    sup = DjangoUser(username='admin_2', id=555)
    sup.set_password('123')
    sup.is_superuser = sup.is_staff = True
    sup.save()
    edik = DjangoUser(username='editor', id=2)
    edik.set_password('123')
    edik.is_staff = True
    for tip in ('add', 'change', 'delete', 'view'):
        for model in ('event', 'rawevent', 'profile', 'subject'):
            perm = Permission.objects.get_by_natural_key(f'{tip}_{model}', 'eventHandler', f'{model}').id
            edik.user_permissions.add(perm)
    edik.save()
    pchel = DjangoUser(username='based', id=3)
    pchel.save()


if __name__ == '__main__':
    pass
    # print(get_subjects())
