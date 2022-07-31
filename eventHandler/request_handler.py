from eventHandler.models import Events, Subjects
from datetime import date


def get_all_this_date(date):
    ev = Events.objects.filter(notify_date=date)
    return ev



if __name__ == '__main__':
    pass
    # print(get_all_this_date())