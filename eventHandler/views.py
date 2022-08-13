import json
import time
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
    QUESTIONS = DATA.questions
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['secret'] == SECRET_KEY_VK:
            print(data['type'])
            print(data)
            if data['type'] == 'confirmation':
                return HttpResponse(CONFIRMATION_TOKEN, content_type='text/plain', status=200)

            elif data['type'] == 'message_new':
                # update_db()
                print(DATA.subjects)
                if time.time() - data['object']['message']['date'] >= 60:
                    return SUCCESS
                auth = vk_api.VkApi(token=TOKEN)
                sender = str(data['object']['message']['from_id'])
                body = data['object']['message']['text']

                if not is_user_in_database(vk_id=sender):
                    create_new_vk_user(sender, None)
                    change_user_question(sender, QUESTIONS[0])
                    COMMANDS_DICT['старт'].reply(sender, auth)

                elif body.lower() == 'меню':
                    COMMANDS_DICT['меню'].reply(sender, auth)
                    change_user_question(sender, QUESTIONS[1])

                elif get_user_question(sender) == str(QUESTIONS[0]):
                    if body.lower() in ['11', '10', '9', '8']:
                        change_user_grade(sender, int(body))
                        change_user_question(sender, QUESTIONS[1])
                        COMMANDS_DICT['меню'].reply(sender, auth)

                elif body.lower() == 'управление рассылкой' \
                        and get_user_question(sender) == str(QUESTIONS[1]):
                    change_user_question(sender, QUESTIONS[2])
                    notifications(sender, auth)
                elif body.lower() == 'включить рассылку' \
                        and get_user_question(sender) == str(QUESTIONS[1]):
                    turn_on_sending(sender)
                    COMMANDS_DICT['success'].reply(sender, auth)
                elif body.lower() == 'отключить рассылку' \
                        and get_user_question(sender) == str(QUESTIONS[1]):
                    turn_off_sending(sender)
                    COMMANDS_DICT['success'].reply(sender, auth)

                elif body.lower() == 'мои рассылки' \
                        and get_user_question(sender) == str(QUESTIONS[2]):
                    COMMANDS_DICT['мои рассылки'].reply(sender, auth, vk_id=True)
                elif (body.lower() == 'добавить уведомления' or body.lower() == 'убрать уведомления') \
                        and get_user_question(sender) == str(QUESTIONS[2]):
                    COMMANDS_DICT['изменить уведомления по предметам'].reply(sender, auth)
                    change_user_question(sender, QUESTIONS[3 + (body.lower() == 'убрать уведомления')])

                elif get_user_question(sender) == str(QUESTIONS[3]) \
                        or get_user_question(sender) == str(QUESTIONS[4]):
                    if not 1 <= int(body.lower()) <= len(DATA.subjects):
                        COMMANDS_DICT['failure'].reply(sender, auth)
                    else:
                        # user = get_user(str(sender))
                        # chosen_sub = DATA.subjects[int(body) - 1]
                        # change_events_by_subject(chosen_sub, user, get_user_question(sender).lower())
                        # change_user_question(sender, QUESTIONS[1])
                        COMMANDS_DICT['Настроить рассылку'].reply(sender, auth, toggle_start=True,
                                                                  chosen_option=int(body))
                        change_user_question(sender, QUESTIONS[5])
                        change_user_chosen_subject(sender, int(body))

                elif get_user_question(sender) == str(QUESTIONS[5]):
                    print(len(get_events_by_subject(get_user_chosen_subject(sender))) + 2)
                    if not 1 <= int(body.lower()) <= len(get_events_by_subject(get_user_chosen_subject(sender))) + 2:
                        COMMANDS_DICT['failure'].reply(sender, auth)
                    else:
                        change_user_events(sender, int(body))
                        COMMANDS_DICT['Настроить рассылку'].reply(sender, auth, toggle_start=True,
                                                                  chosen_option=(generate_list(DATA.subjects).index(
                                                                      str(get_user_chosen_subject(sender))) + 1))

                else:
                    change_user_question(sender, QUESTIONS[1])
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
