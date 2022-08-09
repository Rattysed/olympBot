from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from eventHandler.db_controller import *
from vk_api import VkApi
import os

local_data = {}


class Command:
    def __init__(self, title, action, vk_keyboard: VkKeyboard = None, keyword=''):
        self.title = title
        self.action = action
        self.keyword = keyword
        self.tg_keyboard = None
        self.vk_keyboard = vk_keyboard

    def reply(self, sender, auth, vk=True, **kwargs):
        # TODO: Логгирование прям здесь

        if kwargs.get('huynya_ebanaya', False):
            pass
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
keyboard_notif.add_button('Добавить уведомления', color=VkKeyboardColor.SECONDARY)
keyboard_notif.add_button('Убрать уведомления', color=VkKeyboardColor.SECONDARY)
keyboard_notif.add_line()
keyboard_notif.add_button('Меню', color=VkKeyboardColor.PRIMARY)

keyboard_grades = VkKeyboard(one_time=False)
keyboard_grades.add_button('11', color=VkKeyboardColor.SECONDARY)
keyboard_grades.add_button('10', color=VkKeyboardColor.SECONDARY)
keyboard_grades.add_line()
keyboard_grades.add_button('9', color=VkKeyboardColor.SECONDARY)
keyboard_grades.add_button('8', color=VkKeyboardColor.SECONDARY)


def write_message_with_menu(sender, message, auth):  # функция отправки сообщения + высвечивание кнопки перехода в меню
    auth.method('messages.send', {'user_id': sender, 'message': message,
                                  'random_id': get_random_id(), 'keyboard': keyboard_send_menu.get_keyboard()})


def vk_write_message(sender, auth, message,
                     keyboard: VkKeyboard = None):  # функция отправки сообщения message пользователю sender
    message_data = {'user_id': sender, 'message': message,
                    'random_id': get_random_id()}
    if keyboard is not None:
        message_data['keyboard'] = keyboard.get_keyboard()
    auth.method('messages.send', message_data)


def ask_about_grades():
    return 'В каком вы сейчас классе?'


def send_menu():  # стандартное меню
    return 'Типа меню'


def error_message():
    return 'Неизвестная команда'


def subject_notification():
    all_subs = DATA.subjects[:]
    output = 'Выберите один из предметов ниже:\n\n'
    i = 1
    for sub in all_subs:
        output += str(i) + ') ' + str(sub) + '\n'
        i += 1
    output += '\n(Напишите в чат предмет или соответствующую ему цифру)'
    return output


def choose_subjects(sender, auth):  # меню добавления предметов для рассылки
    auth.method('messages.send', {'user_id': sender, 'message': 'Отлично!\n Выберите предмет, по которому'
                                                                ' хотите получать уведомления.',
                                  'random_id': get_random_id(), 'keyboard': keyboard_choose.get_keyboard()})


def notifications(sender, auth):  # меню управления уведомлениями
    auth.method('messages.send', {'user_id': sender, 'message': 'Заглушка',
                                  'random_id': get_random_id(), 'keyboard': keyboard_notif.get_keyboard()})


def send_info(senders, message, auth):
    for sender in senders:
        auth.method('messages.send', {'user_id': sender, 'message': message,
                                      'random_id': get_random_id()})


TOKEN = os.environ['TOKEN']


def test_action(vk_id='', tg_id=''):
    return 'Тестовая команда'


def make_distribution():
    auth = VkApi(token=TOKEN)
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
        send_info(vk_users, message, auth)


COMMANDS_DICT = {
    'тест': Command('тест', action=test_action, keyword='тест'),
    'старт': Command('ask_about_grades', action=ask_about_grades, vk_keyboard=keyboard_grades),
    'меню': Command('menu', action=send_menu, vk_keyboard=keyboard_menu),
    'wrong': Command('error', action=error_message, vk_keyboard=keyboard_menu),
    'добавить уведомления по предметам': Command('add_notification_sub', action=subject_notification,
                                                 vk_keyboard=keyboard_send_menu),
    'success': Command('success', action=lambda: "Успех!", vk_keyboard=keyboard_send_menu),
    'failure': Command('failure', action=lambda: "Ошибка. Неверное значение"),
}
