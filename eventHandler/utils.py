from bs4 import BeautifulSoup
import requests
from eventHandler.models import *
from typing import Tuple

UA = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML,'
                  ' like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

BAN_WORDS = ['дизайн', 'искусство', 'китайск', 'архитектура', 'восточны',
             'политология', 'психология', 'религиоведение', 'социология',
             'рисунок', 'композиция', 'философия', 'филология', 'востоковедение',
             'музык', 'сольфеджио', 'дирижирование', 'культур', 'юриспруденц',
             'теология', 'педагог', 'журналистика', 'родной язык', 'литература']

BAN_NAMES = ['всероссийская',
             'школьников',
             'междисциплинарная',
             '+сибирского+федерального+округа', ]


def make_rawevent(name, link, profile, subjects, level):
    ev_profile, created = Profile.objects.get_or_create(name=profile)
    if created:
        ev_profile.save()
    if any(map(lambda x: x in profile.lower(), BAN_WORDS)):
        ev_profile.delete()
        return
    new_event, created = RawEvent.objects.get_or_create(name=name, profile=ev_profile)
    if not created:
        return
    new_event.url = link
    new_event.level = level
    new_event.save()
    for s in subjects:
        # print(s.lower())
        if any(map(lambda x: x in s.lower(), BAN_WORDS)):
            ev_profile.delete()
            new_event.delete()
            return
        subject, created = Subject.objects.get_or_create(name=s)
        if created:
            subject.save()
        new_event.subject.add(subject)
    new_event.save()


def suck_from_olimpiada_sru():
    url = 'https://olimpiada.ru/article/993'
    response = requests.get(url, headers=UA)
    soup = BeautifulSoup(response.text, 'lxml')
    tables = soup.find_all('table', class_="note_table")
    for i, table in enumerate(tables):
        if not i:
            continue
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
            subjects = row[3].find('p').text.split(', ')
            level = int(row[4].find('p').text)

            make_rawevent(name, link, profile, subjects, level)


if __name__ == '__main__':
    pass
