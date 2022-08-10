import json
import time
import os
import vk_api
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import EventForm
from .vk_bot.vk_functions import *
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

                if not is_user_in_database(vk_id=sender):
                    create_new_vk_user(sender, None)
                    change_user_question(sender, DATA.questions[0])
                    COMMANDS_DICT['старт'].reply(sender, auth)

                elif body.lower() == 'меню':
                    COMMANDS_DICT['меню'].reply(sender, auth)
                    change_user_question(sender, DATA.questions[1])

                elif get_user_question(sender) == str(DATA.questions[0]):
                    if body.lower() in ['11', '10', '9', '8']:
                        change_user_grade(sender, int(body))
                        change_user_question(sender, DATA.questions[1])
                        COMMANDS_DICT['меню'].reply(sender, auth)

                elif body.lower() == 'управление рассылкой' \
                        and get_user_question(sender) == str(DATA.questions[1]):
                    change_user_question(sender, DATA.questions[2])
                    notifications(sender, auth)
                elif body.lower() == 'включить рассылку' \
                        and get_user_question(sender) == str(DATA.questions[1]):
                    turn_on_sending(sender)
                    COMMANDS_DICT['success'].reply(sender, auth)
                elif body.lower() == 'отключить рассылку' \
                        and get_user_question(sender) == str(DATA.questions[1]):
                    turn_off_sending(sender)
                    COMMANDS_DICT['success'].reply(sender, auth)

                elif body.lower() == 'мои рассылки' \
                        and get_user_question(sender) == str(DATA.questions[2]):
                    COMMANDS_DICT['мои рассылки'].reply(sender, auth, vk_id=True)

                    pass  # TODO показ ВСЕХ рассылок юзера
                elif body.lower() == 'добавить уведомления' \
                        and get_user_question(sender) == str(DATA.questions[2]):
                    COMMANDS_DICT['добавить уведомления по предметам'].reply(sender, auth)
                    change_user_question(sender, DATA.questions[3])

                elif get_user_question(sender) == str(DATA.questions[3]):
                    if not 1 <= int(body.lower()) <= len(DATA.subjects):
                        COMMANDS_DICT['failure'].reply(sender, auth)
                    else:
                        # TODO: Создать функцию-обработчик изменений подписанных ивентов
                        user = get_user(str(sender))
                        chosen_sub = DATA.subjects[int(body) - 1]
                        add_events_by_subject(chosen_sub, user)
                        change_user_question(sender, DATA.questions[1])
                        COMMANDS_DICT['success'].reply(sender, auth)
                        # write_message(sender, 'Параметры рассылки обновлены!', auth)

                else:
                    COMMANDS_DICT['wrong'].reply(sender, auth)

    return SUCCESS


def test(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin")

    if request.method == 'POST':
        eventForm = EventForm(request.POST)
        if eventForm.is_valid():
            for grade in eventForm.cleaned_data['grades']:
                grade = int(grade)
                event = Event()
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
