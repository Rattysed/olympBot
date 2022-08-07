import vk
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from .vk_config import SECRET_KEY, TOKEN, CONFIRMATION_TOKEN
from django.shortcuts import render, HttpResponseRedirect, HttpResponse

local_data = {}

keyboard_menu = VkKeyboard(one_time=True)
keyboard_menu.add_button('Управление рассылкой', color=VkKeyboardColor.PRIMARY)
keyboard_menu.add_line()
keyboard_menu.add_button('Включить рассылку', color=VkKeyboardColor.POSITIVE)
keyboard_menu.add_line()
keyboard_menu.add_button('Отключить рассылку', color=VkKeyboardColor.NEGATIVE)

keyboard_send_menu = VkKeyboard(one_time=True)
keyboard_send_menu.add_button('Меню', color=VkKeyboardColor.PRIMARY)

keyboard_choose = VkKeyboard(one_time=False)
keyboard_choose.add_button('Математика', color=VkKeyboardColor.SECONDARY)
keyboard_choose.add_button('Информатика', color=VkKeyboardColor.SECONDARY)
keyboard_choose.add_line()
keyboard_choose.add_button('Меню', color=VkKeyboardColor.PRIMARY)

keyboard_notif = VkKeyboard(one_time=True)
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
    return HttpResponse('ok', content_type="text/plain", status=200)


def write_message(sender, message, auth):  # функция отправки сообщения message пользователю sender
    auth.method('messages.send', {'user_id': sender, 'message': message,
                                  'random_id': get_random_id()})
    return HttpResponse('ok', content_type="text/plain", status=200)


def ask_about_grades(sender, auth):
    auth.method('messages.send', {'user_id': sender, 'message': 'В каком классе ты учишься?',
                                  'random_id': get_random_id(), 'keyboard': keyboard_grades.get_keyboard()})
    return HttpResponse('ok', content_type="text/plain", status=200)


def send_menu(sender, auth):  # стандартное меню
    auth.method('messages.send', {'user_id': sender, 'message': 'Заглушка для меню',
                                  'random_id': get_random_id(), 'keyboard': keyboard_menu.get_keyboard()})
    return HttpResponse('ok', content_type="text/plain", status=200)


def choose_subjects(sender, auth):  # меню добавления предметов для рассылки
    auth.method('messages.send', {'user_id': sender, 'message': 'Отлично!\n Выберите предмет, по которому'
                                                                ' хотите получать уведомления.',
                                  'random_id': get_random_id(), 'keyboard': keyboard_choose.get_keyboard()})
    return HttpResponse('ok', content_type="text/plain", status=200)


def notifications(sender, message, auth):  # меню управления уведомлениями
    auth.method('messages.send', {'user_id': sender, 'message': message,
                                  'random_id': get_random_id(), 'keyboard': keyboard_notif.get_keyboard()})
    return HttpResponse('ok', content_type="text/plain", status=200)


def add_to_local_data(id, question):
    p = {
        'id': id,
        'question': question
    }
    local_data[id] = p
    return
