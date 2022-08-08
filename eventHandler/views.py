import json
import time
import os
import vk_api
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import EventForm
from .bot_handler import make_distribution
from .vk_bot.vk_functions import write_message, send_menu, ask_about_grades, \
    add_to_local_data, local_data, notifications, write_message_with_menu
from .db_controller import *

SUCCESS = HttpResponse('ok', content_type='text/plain', status=200)
SECRET_KEY_VK = os.environ['SECRET_KEY_VK']
CONFIRMATION_TOKEN = os.environ['CONFIRMATION_TOKEN']
TOKEN = os.environ['TOKEN']


@csrf_exempt
def vk_bot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['secret'] == SECRET_KEY_VK:
            print(data['type'])
            print(data)
            if data['type'] == 'confirmation':
                return HttpResponse(CONFIRMATION_TOKEN, content_type='text/plain', status=200)

            elif data['type'] == 'message_new':
                if time.time() - data['object']['message']['date'] >= 60:
                    return SUCCESS
                auth = vk_api.VkApi(token=TOKEN)
                sender = str(data['object']['message']['from_id'])
                body = data['object']['message']['text']

                if sender not in local_data:
                    add_to_local_data(sender, 0)
                    local_data[sender]['question'] = 1
                    ask_about_grades(sender, auth)

                elif local_data[sender]['question'] == 1 \
                        and not is_user_in_database(vk_id=sender):
                    if body.lower() in ['11', '10', '9', '8']:
                        create_new_vk_user(sender, int(body.lower()))
                        local_data[sender]['question'] = 2
                        send_menu(sender, auth)
                elif local_data[sender]['question'] == 1 \
                        and is_user_in_database(vk_id=sender):
                    if body.lower() in ['11', '10', '9', '8']:
                        # TODO изменить класс юзера

                        local_data[sender]['question'] = 2
                        send_menu(sender, auth)

                elif body.lower() == 'управление рассылкой' \
                        and local_data[sender]['question'] == 2:
                    local_data[sender]['question'] = 3
                    notifications(sender, auth)
                elif body.lower() == 'включить рассылку' \
                        and local_data[sender]['question'] == 2:
                    pass  # TODO включение рассылки
                elif body.lower() == 'отключить рассылку' \
                        and local_data[sender]['question'] == 2:
                    pass  # TODO отключение рассылки

                elif body.lower() == 'мои рассылки' \
                        and local_data[sender]['question'] == 3:
                    pass  # TODO показ ВСЕХ рассылок юзера
                elif body.lower() == 'добавить уведомления' \
                        and local_data[sender]['question'] == 3:
                    all_subs = DATA.subjects[:]
                    output = 'Выберите один из предметов ниже:\n\n'
                    i = 1
                    for sub in all_subs:
                        output += str(i) + ') ' + str(sub) + '\n'
                        i += 1
                    output += '\n(Напишите в чат предмет или соответствующую ему цифру)'
                    local_data[sender]['question'] = 4
                    write_message_with_menu(sender, output, auth)

                elif local_data[sender]['question'] == 4:
                    if not 1 <= int(body.lower()) <= len(DATA.subjects):
                        write_message(sender, 'Неверный диапазон', auth)
                    else:
                        user = get_user(str(sender))
                        chosen_sub = DATA.subjects[int(body) - 1]
                        add_events_by_subject(chosen_sub, user)
                        write_message(sender, 'Параметры рассылки обновлены!', auth)

                else:
                    pass

    return SUCCESS


def test(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin")

    if request.method == 'POST':
        eventForm = EventForm(request.POST)
        if eventForm.is_valid():
            for grade in eventForm.cleaned_data['grades']:
                grade = int(grade)
                event = Events()
                event.name = eventForm.cleaned_data['name']
                event.notify_date = eventForm.cleaned_data['notify_date']
                event.period = eventForm.cleaned_data['period']
                event.level = eventForm.cleaned_data['event_level']
                event.event_priority = eventForm.cleaned_data['priority']
                event.save()
                for sub in eventForm.cleaned_data['subject']:
                    event.subject.add(int(sub))
                for prof in eventForm.cleaned_data['profile']:
                    event.profile.add(int(prof))
                event.event_grade = grade
                try:
                    event.next_event_id = int(eventForm.cleaned_data['next_event'])
                except:
                    print('Nope')
                event.event_url = eventForm.cleaned_data['event_url']
                event.description = eventForm.cleaned_data['description']
                event.save()
            return HttpResponse('Добавили')
            pass
        else:

            return HttpResponse(eventForm.errors)
            pass

    eventForm = EventForm()

    return render(request, 'test.html', {'form': eventForm})


def bot_test(request):
    make_distribution()
    return HttpResponse('С кайфом')
