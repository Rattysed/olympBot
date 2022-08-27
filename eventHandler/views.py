import json
import time
import vk_api
from eventHandler.utils import *
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import EventForm
from .vk_bot.vk_functions import *
from .db_controller import *

SUCCESS = HttpResponse('ok', content_type='text/plain', status=200)
SECRET_KEY_VK = os.environ['SECRET_KEY_VK']
CONFIRMATION_TOKEN = os.environ['CONFIRMATION_TOKEN']
TOKEN = os.environ['TOKEN']
setup_db()


@csrf_exempt
def vk_bot(request):
    QUESTIONS = DATA.questions
    if request.method == 'POST':
        data = json.loads(request.body)
        if data['secret'] == SECRET_KEY_VK:
            print(data['type'])
            print(data)
            print(QUESTIONS)
            if data['type'] == 'confirmation':
                return HttpResponse(CONFIRMATION_TOKEN, content_type='text/plain', status=200)

            elif data['type'] == 'message_new':
                print(get_all_this_grade_today(11))
                if time.time() - data['object']['message']['date'] >= 60:
                    return SUCCESS
                auth = vk_api.VkApi(token=TOKEN)
                sender = str(data['object']['message']['from_id'])
                body = data['object']['message']['text']
                print(get_main_events_of_user(sender))

                if not is_user_in_database(vk_id=sender):
                    create_new_vk_user(sender, None)
                    change_user_question(sender, QUESTIONS[0])
                    COMMANDS_DICT['приветствие'].reply(sender, auth)
                    COMMANDS_DICT['сменить класс'].reply(sender, auth)

                elif body.lower() == 'меню':
                    COMMANDS_DICT['меню'].reply(sender, auth)
                    change_user_question(sender, QUESTIONS[1])
                elif body.lower() == 'назад':
                    if not is_empty_rollback_question(get_rollback_question(sender)):
                        COMMANDS_DICT[get_current_rollback(sender)[0].get('rollback_command',
                                                                          False)].reply(sender, auth)
                        change_user_question(sender, get_rollback_question(sender), is_string=True)
                    else:
                        COMMANDS_DICT['wrong'].reply(sender, auth)

                elif str(get_user_question(sender)) == str(QUESTIONS[0]):
                    if body.lower() in ['11', '10', '9', '8']:
                        change_user_grade(sender, int(body))
                        change_user_question(sender, QUESTIONS[1])
                        COMMANDS_DICT['меню'].reply(sender, auth)

                elif body.lower() == 'текущие регистрации' \
                        and str(get_user_question(sender)) == str(QUESTIONS[1]):
                    COMMANDS_DICT['в разработке'].reply(sender, auth)

                elif body.lower() == 'управление рассылкой' \
                        and str(get_user_question(sender)) == str(QUESTIONS[1]):
                    change_user_question(sender, QUESTIONS[2])
                    COMMANDS_DICT['меню уведомлений'].reply(sender, auth)
                elif body.lower() == '🔔' \
                        and str(get_user_question(sender)) == str(QUESTIONS[1]):
                    turn_on_sending(sender)
                    COMMANDS_DICT['success'].reply(sender, auth)
                elif body.lower() == '🔕' \
                        and str(get_user_question(sender)) == str(QUESTIONS[1]):
                    turn_off_sending(sender)
                    COMMANDS_DICT['success'].reply(sender, auth)

                elif body.lower() == 'мои рассылки' \
                        and str(get_user_question(sender)) == str(QUESTIONS[2]):
                    COMMANDS_DICT['мои рассылки'].reply(sender, auth, vk_id=True)
                elif (body.lower() == 'добавить/изменить' or body.lower() == 'убрать') \
                        and str(get_user_question(sender)) == str(QUESTIONS[2]):
                    COMMANDS_DICT['изменить уведомления по предметам'].reply(sender, auth)
                    change_user_question(sender, QUESTIONS[3 + (body.lower() == 'убрать')])
                elif body.lower() == 'сменить класс' \
                        and str(get_user_question(sender)) == str(QUESTIONS[2]):
                    change_user_question(sender, QUESTIONS[7])
                    COMMANDS_DICT['предупреждение'].reply(sender, auth)

                elif str(get_user_question(sender)) == str(QUESTIONS[3]) \
                        or str(get_user_question(sender)) == str(QUESTIONS[4]):
                    print(get_subevents_by_subject_and_grade(sender, get_user_chosen_subject(sender)))
                    if not 1 <= int(body.lower()) <= len(DATA.subjects):
                        COMMANDS_DICT['failure'].reply(sender, auth)
                    else:
                        change_user_chosen_subject(sender, int(body))
                        if str(get_user_question(sender)) == str(QUESTIONS[3]):
                            COMMANDS_DICT['настроить рассылку'].reply(sender, auth, toggle_start=True,
                                                                      chosen_option=int(body))
                            change_user_question(sender, QUESTIONS[5])
                        elif str(get_user_question(sender)) == str(QUESTIONS[4]):
                            COMMANDS_DICT['настроить рассылку'].reply(sender, auth, toggle_start=True,
                                                                      chosen_option=int(body), remove=True)
                            change_user_question(sender, QUESTIONS[6])

                elif str(get_user_question(sender)) == str(QUESTIONS[5]):
                    print(get_events_of_user(sender))
                    if not 1 <= int(body.lower()) <= len(get_events_by_subject(get_user_chosen_subject(sender))) + 2:
                        COMMANDS_DICT['failure'].reply(sender, auth)
                    else:
                        change_user_events(sender, int(body))
                        COMMANDS_DICT['настроить рассылку'].reply(sender, auth, toggle_start=True,
                                                                  chosen_option=(generate_list(DATA.subjects).index(
                                                                      str(get_user_chosen_subject(sender))) + 1))
                elif str(get_user_question(sender)) == str(QUESTIONS[6]):
                    if not 1 <= int(body.lower()) <= len(
                            get_events_of_user(sender).get(str(get_user_chosen_subject(sender)), [])):
                        COMMANDS_DICT['failure'].reply(sender, auth)
                    else:
                        remove_user_events(sender, int(body))
                        COMMANDS_DICT['настроить рассылку'].reply(sender, auth, toggle_start=True,
                                                                  chosen_option=(generate_list(DATA.subjects).index(
                                                                      str(get_user_chosen_subject(sender))) + 1),
                                                                  remove=True)

                elif str(get_user_question(sender)) == str(QUESTIONS[7]) \
                        and body.lower() == 'да':
                    change_user_question(sender, QUESTIONS[0])
                    drop_events_of_user(sender)
                    COMMANDS_DICT['сменить класс'].reply(sender, auth)
                elif str(get_user_question(sender)) == str(QUESTIONS[7]) \
                        and body.lower() == 'назад':
                    change_user_question(sender, QUESTIONS[2])
                    COMMANDS_DICT['меню уведомлений'].reply(sender, auth)

                else:
                    # change_user_question(sender, QUESTIONS[1])
                    COMMANDS_DICT['wrong'].reply(sender, auth)

    return SUCCESS


def test(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin")

    if request.method == 'POST':
        return HttpResponse('Да ебись ты в рот')
    eventForm = EventForm()

    return render(request, 'test.html', {'form': eventForm})


def bot_test(request):
    # get_olymps_from_rsosh()
    find_grades_of_event(RawEvent.objects.get(id=151))
    return HttpResponse('С кайфом')
