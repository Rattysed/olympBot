from eventHandler.models import Events, Subjects, User
import datetime


def get_all_this_date(date):
    ev = Events.objects.filter(notify_date=datetime.date)
    return ev


def get_all_today():
    return get_all_this_date(datetime.date.today())


def create_new_user(grade, vk_id='', tg_id=''):
    if vk_id == tg_id == '':
        return AttributeError("Can't create user without any messenger account")
    user = User()
    user.vk_id = vk_id
    user.tg_id = tg_id
    user.grade = grade
    user.save()


def create_new_vk_user(id, grade):
    create_new_user(grade, vk_id=id)


def create_new_tg_user(id, grade):
    create_new_user(grade, tg_id=id)


if __name__ == '__main__':
    pass
    # print(get_all_this_date())
