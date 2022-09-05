from bs4 import BeautifulSoup
import requests
from eventHandler.models import *
from typing import Tuple
import datetime

UA = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML,'
                  ' like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

EVENT_SOURCE = 'https://olimpiada.ru/article/993'

BAN_WORDS = ['дизайн', 'искусство', 'китайск', 'архитектура', 'восточны',
             'политология', 'психология', 'религиоведение', 'социология',
             'рисунок', 'композиция', 'философия', 'филология', 'востоковедение',
             'музык', 'сольфеджио', 'дирижирование', 'культур', 'юриспруденц',
             'теология', 'педагог', 'журналистика', 'родной язык', ]

BAN_NAMES = ['Филология', 'Дизайн', 'Искусство и изо', 'Музыка', 'Политология', 'Психология',
             'Социология', 'Геология', ]

CUR_STUDY_YEAR = datetime.date.today().year  # Год начала текущего учебного года
if datetime.date.today().month < 6:
    CUR_STUDY_YEAR -= 1
MONTH_TO_DATE = {
    'янв': datetime.date(CUR_STUDY_YEAR + 1, 1, 1),
    'фев': datetime.date(CUR_STUDY_YEAR + 1, 2, 1),
    'мар': datetime.date(CUR_STUDY_YEAR + 1, 3, 1),
    'апр': datetime.date(CUR_STUDY_YEAR + 1, 4, 1),
    'май': datetime.date(CUR_STUDY_YEAR + 1, 5, 1),
    'июн': datetime.date(CUR_STUDY_YEAR, 6, 1),
    'июл': datetime.date(CUR_STUDY_YEAR, 7, 1),
    'авг': datetime.date(CUR_STUDY_YEAR, 8, 1),
    'сен': datetime.date(CUR_STUDY_YEAR, 9, 1),
    'окт': datetime.date(CUR_STUDY_YEAR, 10, 1),
    'ноя': datetime.date(CUR_STUDY_YEAR, 11, 1),
    'дек': datetime.date(CUR_STUDY_YEAR, 12, 1),
}


def make_rawevent(name, link, profile, level):
    ev_profile, created = Profile.objects.get_or_create(name=profile)
    if created:
        ev_profile.save()
    if any(map(lambda x: x in profile.lower(), BAN_WORDS)):
        ev_profile.delete()
        return
    new_event, created = RawEvent.objects.get_or_create(name=name, profile=ev_profile)
    if not created:
        return new_event
    new_event.url = link
    new_event.level = level
    return new_event


def get_from_olimiada_ru():
    url = EVENT_SOURCE
    response = requests.get(url, headers=UA)
    soup = BeautifulSoup(response.text, 'lxml')
    tables = soup.find_all('table', class_="note_table")
    first_table = soup.find('table', class_="note_table")
    p_shki = first_table.find_next_siblings('p')
    for i, table in enumerate(tables):
        if not i:
            continue
        sub = p_shki[i - 1].text
        if sub in BAN_NAMES:
            continue
        subject, created = Subject.objects.get_or_create(name=sub)
        if created:
            subject.save()
        print(f'Пошла таблица {i} из {len(tables) - 1}')
        t_rows = table.find_all('tr')
        for j, row in enumerate(t_rows):
            if not j:
                continue
            print(f'\tПошла строка {j} из {len(t_rows) - 1}')
            row = list(row.find_all('td'))
            name = row[0].find('p').text
            link = 'https://olimpiada.ru' + row[0].find('a')['href']
            profile = row[2].find('p').text
            level = int(row[4].find('p').text)
            event = make_rawevent(name, link, profile, level)
            if event is None:
                continue
            event.save()
            event.subject.add(subject)
            event.save()


def get_event_data(event: RawEvent):
    response = requests.get(event.url)
    soup = BeautifulSoup(response.text, 'lxml')
    events_table = soup.find('table', class_='events_for_activity')
    grades = soup.find('span', class_='classes_types_a').text
    nums = grades.split()[0]
    try:
        min_grade = max(int(nums.split('–')[0]), 9)
        max_grade = int(nums.split('–')[1])
    except:
        min_grade = max_grade = int(nums)
    event.min_grade = min_grade
    event.max_grade = max_grade
    event.save()
    print(event.name)
    last_ev = None
    if events_table is not None:
        event_rows = events_table.find_all('tr', class_='notgreyclass')
        for row in event_rows:
            row = list(row.find_all('a'))
            name = row[0].text
            date = row[1].text
            if 'до' in date.lower() or 'junior' in name.lower():
                continue
            print(date, list(row))
            if '...' in date:
                start, finish = date.split('...')
            else:
                start = date
                finish = False
            try:
                start_day, start_month = start.split()
            except:
                finish_day, finish_month = finish.split()
                start_day = start
                start_month = finish_month
            start_date = MONTH_TO_DATE[start_month.lower()] + datetime.timedelta(days=int(start_day) - 2)
            start_event, s_c = Event.objects.get_or_create(name=name, notify_date=start_date, url=event.url,
                                                           description=event.description)
            start_event.save()
            if last_ev is not None:
                last_ev.next_event_id = start_event
                last_ev.save()
            last_ev = start_event
            if finish:
                finish_day, finish_month = finish.split()
                finish_date = MONTH_TO_DATE[finish_month.lower()] + datetime.timedelta(days=int(finish_day) - 2)
                finish_event, f_c = Event.objects.get_or_create(name="Конец события " + name, notify_date=finish_date,
                                                                url=event.url,
                                                                description=event.description)
                finish_event.save()
                start_event.next_event_id = finish_event
                last_ev = finish_event
            start_event.save()


def add_rawevents_data():
    events = RawEvent.objects.filter()
    for num, ev in enumerate(events):
        # if num >15:
        #     break
        # if num < 15:
        #     continue
        print(f"{num + 1}/{len(events)}")
        get_event_data(ev)

    pass


if __name__ == '__main__':
    pass
