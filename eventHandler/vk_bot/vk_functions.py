from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from eventHandler.db_controller import *
from typing import List, Union
from vk_api import VkApi
import os

TOKEN = os.environ['TOKEN']


class Command:
    def __init__(self, title, action, vk_keyboard: VkKeyboard = None, keyword=''):
        self.title = title
        self.action = action
        self.keyword = keyword
        self.tg_keyboard = None
        self.vk_keyboard = vk_keyboard

    def reply(self, sender, auth, vk=True, **kwargs):
        # TODO: Логгирование прям здесь
        message = ''
        print(kwargs)
        print(kwargs.get('toggle_start', False))
        if kwargs.get('huynya_ebanaya', False):
            pass
        elif kwargs.get('toggle_start', False):
            if kwargs.get('remove', False):
                message = self.action(sender, kwargs.get('chosen_option', -1), remove=True)
            else:
                message = self.action(sender, kwargs.get('chosen_option', -1))
        elif kwargs.get('vk_id', False):
            message = self.action(sender)
        else:
            message = self.action()
        if vk:
            vk_write_message(sender, auth, message, keyboard=self.vk_keyboard)
        else:
            pass


keyboard_menu = VkKeyboard(one_time=False)
keyboard_menu.add_button('Управление рассылкой', color=VkKeyboardColor.PRIMARY)
keyboard_menu.add_line()
keyboard_menu.add_button('Включить рассылку', color=VkKeyboardColor.POSITIVE)
keyboard_menu.add_line()
keyboard_menu.add_button('Отключить рассылку', color=VkKeyboardColor.NEGATIVE)

keyboard_send_menu = VkKeyboard(one_time=False)
keyboard_send_menu.add_button('Меню', color=VkKeyboardColor.PRIMARY)

keyboard_choose = VkKeyboard(one_time=False)
keyboard_choose.add_button('Математика', color=VkKeyboardColor.SECONDARY)
keyboard_choose.add_button('Информатика', color=VkKeyboardColor.SECONDARY)
keyboard_choose.add_line()
keyboard_choose.add_button('Меню', color=VkKeyboardColor.PRIMARY)

keyboard_notif = VkKeyboard(one_time=False)
keyboard_notif.add_button('Мои рассылки', color=VkKeyboardColor.PRIMARY)
keyboard_notif.add_line()
keyboard_notif.add_button('Добавить/изменить', color=VkKeyboardColor.POSITIVE)
keyboard_notif.add_button('Убрать', color=VkKeyboardColor.NEGATIVE)
keyboard_notif.add_line()
keyboard_notif.add_button('Меню', color=VkKeyboardColor.PRIMARY)

keyboard_grades = VkKeyboard(one_time=False)
keyboard_grades.add_button('11', color=VkKeyboardColor.SECONDARY)
keyboard_grades.add_button('10', color=VkKeyboardColor.SECONDARY)
keyboard_grades.add_line()
keyboard_grades.add_button('9', color=VkKeyboardColor.SECONDARY)
keyboard_grades.add_button('8', color=VkKeyboardColor.SECONDARY)


def vk_write_message(sender, auth, message,
                     keyboard: VkKeyboard = None):  # функция отправки сообщения message пользователю sender
    message_data = {'user_id': sender, 'message': message,
                    'random_id': get_random_id()}
    if keyboard is not None:
        message_data['keyboard'] = keyboard.get_keyboard()
    auth.method('messages.send', message_data)


def ask_about_grades():
    return '(Тут будет красивое приветствие + вопрос про класс обучения)'


def send_menu():  # стандартное меню
    return '(Тут будет описание кнопок и основные принципы работы бота)'


def error_message():
    return 'Неизвестная команда!'


def notifications():  # меню управления уведомлениями
    return 'Красивое описание кнопочек управления уведомлениями'


def subject_notification():
    all_subs = DATA.subjects[:]
    output = 'Выберите один из предметов ниже:\n\n'
    i = 1
    for sub in all_subs:
        output += str(i) + ') ' + str(sub) + '\n'
        i += 1
    output += '\n(Напишите в чат цифру)'
    return output


def show_distributions(sender):
    events_of_user = get_events_of_user(sender)  # set of tuples
    print(events_of_user)
    is_dist = is_distribution(sender)
    output = 'Ваши рассылки:\n\n'
    if not is_dist:
        output += '❗Внимание: Для того, чтобы вам приходили оповещения, необходимо включить рассылку.' \
                  ' Чтобы ее включить, перейдите ' \
                  'в меню и нажмите кнопку "Включить рассылку" \n\n'
    if len(events_of_user.keys()) == 0:
        output = 'Рассылок нет.'
    for sub in DATA.subjects[:]:
        evs = events_of_user.get(sub.name, [])
        print(evs)
        if len(evs) == 0:
            continue
        output += f'{sub.name}:\n'
        for num, ev in enumerate(evs):
            output += f'\t{num + 1}) {ev.name}\n'
    return output


def send_info(senders, message, auth):  # ФУНКЦИЯ РАССЫЛКИ
    for sender in senders:
        auth.method('messages.send', {'user_id': sender, 'message': message,
                                      'random_id': get_random_id()})


def test_action(vk_id='', tg_id=''):
    return 'Тестовая команда'


def make_distribution():
    auth = VkApi(token=TOKEN)
    events = get_all_today()
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
        send_info(vk_users, message, auth)


def toggle_distribution(user_id: int, chosen_subject: int, **kwargs):
    user = get_user(vk_id=str(user_id))
    subject = DATA.subjects[chosen_subject - 1]
    events = get_events_by_subject(subject)
    is_remove = kwargs.get('remove', False)
    if not is_remove:
        output = "Выберите вариант из предложенных:\n\n1) Включить все\n2) Выключить все\n"
        for n, ev in enumerate(events):
            output += f"{n + 3}) {ev.name}"
            if user.events.filter(id=ev.id):
                output += ' ✅\n'
            else:
                output += ' 🚫\n'
        is_dist = is_distribution(user_id)
        if not is_dist:
            output += '\n❗Внимание: Для того, чтобы вам приходили оповещения, необходимо включить рассылку.' \
                      ' Чтобы ее включить, перейдите ' \
                      'в меню и нажмите кнопку "Включить рассылку" \n\n'
        return output
    else:
        n = 1
        output = 'Выберите вариант из предложенных (выбранная олимпиада будет удалена из вашей рассылки):\n\n'
        for ev in events:
            if user.events.filter(id=ev.id):
                output += f"{n}) {ev.name}"
                output += ' ✅\n'
                n += 1
        if n == 1:
            return 'У вас нет активных рассылок по этому предмету.'
        is_dist = is_distribution(user_id)
        if not is_dist:
            output += '\n❗Внимание: Для того, чтобы вам приходили оповещения, необходимо включить рассылку.' \
                      ' Чтобы ее включить, перейдите ' \
                      'в меню и нажмите кнопку "Включить рассылку" \n\n'
        return output


COMMANDS_DICT = {
    'тест': Command('тест', action=test_action, keyword='тест'),
    'старт': Command('ask_about_grades', action=ask_about_grades, vk_keyboard=keyboard_grades),
    'меню': Command('menu', action=send_menu, vk_keyboard=keyboard_menu),
    'wrong': Command('error', action=error_message),
    'изменить уведомления по предметам': Command('change_notification_sub', action=subject_notification,
                                                 vk_keyboard=keyboard_send_menu),
    'success': Command('success', action=lambda: "Параметры обновлены!", vk_keyboard=keyboard_menu),
    'failure': Command('failure', action=lambda: "Ошибка. Введенное значение не принадлежит допустимому диапазону."),
    'мои рассылки': Command('my_distributions', action=show_distributions),
    'настроить рассылку': Command('toggle_distribution', action=toggle_distribution),
    'меню уведомлений': Command('notification_menu', action=notifications, vk_keyboard=keyboard_notif),
}
