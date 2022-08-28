from bs4 import BeautifulSoup
import requests
from eventHandler.models import *
from typing import Tuple

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



if __name__ == '__main__':
    pass
