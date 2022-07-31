import vk_api, time, datetime
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sqlite3 as sql


keyboard_menu = VkKeyboard(one_time=True)
keyboard_menu.add_button('Включить рассылку', color=VkKeyboardColor.POSITIVE)
keyboard_menu.add_line()
keyboard_menu.add_button('Отключить рассылку', color=VkKeyboardColor.NEGATIVE)

# TODO: показ всех доступных событий
# TODO: keyboard_menu.add_line()
# TODO: keyboard_menu.add_button('События')

keyboard_send_menu = VkKeyboard(one_time=True)
keyboard_send_menu.add_button('Меню', color=VkKeyboardColor.PRIMARY)


def add_sub(id, is_rassylka):
    p = {
        'is_rassylka': is_rassylka
    }
    data[id] = p
    return


def write_message(sender, message):
    auth.method('messages.send', {'user_id': sender, 'message': message,
                                  'random_id': get_random_id(), 'keyboard': keyboard_send_menu.get_keyboard()})


def send_menu(sender):
    auth.method('messages.send', {'user_id': sender, 'message': 'Заглушка для меню',
                                  'random_id': get_random_id(), 'keyboard': keyboard_menu.get_keyboard()})


def get_events():
    pass


id_for_send = set()
token = 'vk1.a.Yht64Peg4WcAqBKXBr1Rh0gAySG95jBIhkxGRgPUBAt6jdjGNbDDOHzPy9JA9mPYgXYgK2RZQGa3wWuWfCnJI4nrzQFcRMj5Mqy3zst5jYYdTszIYYEhK65T91Mrt409nwtLVz51MvMT8O4rY6GhzJ77sj3Cem-nO27TXyFBzPMvDHPKtLso-GxVMvmsqbcz'
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
                        break
                if not f:
                    add_sub(sender, False)
                    print(data)

                send_menu(sender)

            elif body.lower() == 'включить рассылку':
                if data[sender]['is_rassylka']:
                    write_message(sender, 'У вас уже подключена рассылка')
                else:
                    data[sender]['is_rassylka'] = True
                    write_message(sender, 'Рассылка успешно подключена!')
                print(data)

            elif body.lower() == 'отключить рассылку':
                if not data[sender]['is_rassylka']:
                    write_message(sender, 'У вас не подключена рассылка')
                else:
                    data[sender]['is_rassylka'] = False
                    write_message(sender, 'Рассылка успешно отключена!')
                print(data)

    except Exception as E:
        time.sleep(1)