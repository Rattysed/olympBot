import vk_api, time, datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3 as sql


keyboard_menu = VkKeyboard(one_time=True)
keyboard_menu.add_button('Включить рассылку', color=VkKeyboardColor.POSITIVE)
keyboard_menu.add_line()
keyboard_menu.add_button('Отключить рассылку', color=VkKeyboardColor.NEGATIVE)
keyboard_menu.add_line()
keyboard_menu.add_button('Мои уведомления', color=VkKeyboardColor.PRIMARY)

# TODO: показ всех доступных событий
# TODO: keyboard_menu.add_line()
# TODO: keyboard_menu.add_button('События')

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


def add_sub(id, is_rassylka, subjects, is_choosing):
    p = {
        'is_rassylka': is_rassylka,
        'subjects': subjects,
        'is_choosing': is_choosing  # нужно для того, чтобы в выбранные предметы
                                    # пользователя случайно не попали предметы до того, как он включит рассылку.
                                    # ничего умнее я не смог придумать чтобы пофиксить это :)
    }
    data[id] = p
    return


def write_message_with_menu(sender, message):  # функция отправки сообщения + высвечивание кнопки перехода в меню
    auth.method('messages.send', {'user_id': sender, 'message': message,
                                  'random_id': get_random_id(), 'keyboard': keyboard_send_menu.get_keyboard()})


def write_message(sender, message):  # функция отправки сообщения message пользователю sender
    auth.method('messages.send', {'user_id': sender, 'message': message,
                                  'random_id': get_random_id()})


def send_menu(sender):  # стандартное меню
    auth.method('messages.send', {'user_id': sender, 'message': 'Заглушка для меню',
                                  'random_id': get_random_id(), 'keyboard': keyboard_menu.get_keyboard()})


def choose_subjects(sender):  # меню добавления предметов для рассылки
    auth.method('messages.send', {'user_id': sender, 'message': 'Отлично!\n Выберите предмет, по которому'
                                                                ' хотите получать уведомления.',
                                  'random_id': get_random_id(), 'keyboard': keyboard_choose.get_keyboard()})


def notifications(sender, message):  # меню управления уведомлениями
    auth.method('messages.send', {'user_id': sender, 'message': message,
                                  'random_id': get_random_id(), 'keyboard': keyboard_notif.get_keyboard()})


def get_events():
    pass


id_for_send = set()
token = 'vk1.a.Yht64Peg4WcAqBKXBr1Rh0gAySG95jBIhkxGRg' \
        'PUBAt6jdjGNbDDOHzPy9JA9mPYgXYgK2RZQGa3wWuWfCnJI4nrzQFcRMj5M' \
        'qy3zst5jYYdTszIYYEhK65T91Mrt409nwtLVz51MvMT8O4rY6GhzJ77sj3Cem-nO27TXyFBzPMvDHPKtLso-GxVMvmsqbcz'
auth = vk_api.VkApi(token=token)
longpoll = VkLongPoll(auth)
data = {}

while True:
    try:
        messages = auth.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:
            sender = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]
            if body.lower() == "начать" or "привет" in body.lower() or body.lower() == "меню":
                f = False
                for elem in data:
                    if sender == elem:
                        f = True
                        data[sender]['is_choosing'] = False
                        break
                if not f:
                    add_sub(sender, False, set(), False)  # добавление юзера в БД с дефолтными показателями
                    print(data)

                send_menu(sender)

            elif body.lower() == 'включить рассылку':
                if data[sender]['is_rassylka']:
                    write_message_with_menu(sender, 'У вас уже подключена рассылка')
                else:
                    data[sender]['is_rassylka'] = True
                    write_message(sender, 'Рассылка успешно подключена!')
                    choose_subjects(sender)
                    data[sender]['is_choosing'] = True

                print(data)

            elif body.lower() == 'отключить рассылку':
                if not data[sender]['is_rassylka']:
                    write_message_with_menu(sender, 'У вас не подключена рассылка')
                else:
                    data[sender]['is_rassylka'] = False
                    write_message_with_menu(sender, 'Рассылка успешно отключена!')
                print(data)

            elif body.lower() == 'математика' and data[sender]['is_choosing']:
                data[sender]['subjects'].add('математика')
                write_message(sender, 'Уведомления успешно подключены!')
                print(data)
            elif body.lower() == 'информатика' and data[sender]['is_choosing']:
                data[sender]['subjects'].add('информатика')
                write_message(sender, 'Уведомления успешно подключены!')
                print(data)

            elif body.lower() == 'мои уведомления':
                if not data[sender]['is_rassylka']:
                    write_message_with_menu(sender, 'Упс. Кажется, вы не включили рассылку!')
                else:
                    if len(data[sender]['subjects']) == 0:
                        write_message_with_menu(sender, 'На данный момент у вас нет уведомлений.')
                    else:
                        notifications(sender, 'Ваши уведомления: \n' + ', '.join(data[sender]['subjects']))

    except Exception as E:
        time.sleep(1)