from eventHandler.models import Events, Subjects
import datetime


def get_all_this_date(date):
    ev = Events.objects.filter(notify_date=datetime.date)
    return ev


def get_all_today():
    return get_all_this_date(datetime.date.today())


if __name__ == '__main__':
    pass
    # print(get_all_this_date())
