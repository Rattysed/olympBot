from bs4 import BeautifulSoup
import requests
from eventHandler.models import *
from typing import Tuple

UA = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML,'
                  ' like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

BAN_WORDS = ['литература', 'дизайн', 'искусство', 'китайск',
             'политология', 'экология', 'психология', 'религиоведение',
             'рисунок', 'композиция', 'философия', 'филология', 'востоковедение',
             'музык', 'сольфеджио', 'дирижирование', 'генетика', 'культур', 'юриспруденц',
             'теология', 'педагог', 'журналистика', 'география', 'право']

BAN_NAMES = ['всероссийская',
             'школьников',
             'междисциплинарная',
             '+сибирского+федерального+округа', ]


def get_olymps_from_rsosh():
    result = []
    url = 'https://rsr-olymp.ru'
    response = requests.get(url, headers=UA)

    soup = BeautifulSoup(response.text, 'lxml')
    table = soup.find('div', id='main_table')
    table_rows = table.find_all('tr')
    last_olymp = last_olymp_link = ''
    for row in table_rows[1:]:
        tds = list(row.find_all('td'))
        delta = 0
        if len(tds) == 5:
            last_olymp = tds[1].text
            last_olymp_link = tds[1].find('a')['href']
            delta = 2
        prof = tds[delta].text
        sub = tds[delta + 1].text
        lvl = tds[delta + 2].text
        flag = False
        for b_w in BAN_WORDS:
            if b_w in sub:
                flag = True
                break
        if flag:
            continue
        result.append((last_olymp, last_olymp_link, prof, sub, lvl))
    for id, ev in enumerate(result):
        raw_event = RawEvent(id=id + 1, name=ev[0], url=ev[1], level=int(ev[4]))
        prof = ev[2]
        profile, created = Profile.objects.get_or_create(name=prof)
        if created:
            profile.save()
        raw_event.profile = profile
        subs = ev[3].split(', ')
        raw_event.save()
        for s in subs:
            subject, created = Subject.objects.get_or_create(name=s)
            if created:
                subject.save()
            raw_event.subject.add(subject)
        raw_event.save()


def generate_search_name(name: str) -> str:
    search_name = ''
    for s in name:
        if s.isalnum():
            search_name += s.lower()
        else:
            search_name += '+'
    for nam in BAN_NAMES:
        search_name = search_name.replace(nam, '')

    while '++' in search_name:
        search_name = search_name.replace('++', '+')
    if not search_name[-1].isalnum():
        search_name = search_name[:-1]
    if not search_name[0].isalnum():
        search_name = search_name[0:]
    return search_name


def find_grades_of_event(event: RawEvent):
    if event.min_grade is not None:
        return
    # print(event.min_grade, event.min_grade is not None)
    name = event.name
    search_name = generate_search_name(name)

    # print(search_name)
    url = 'https://olimpiada.ru/search?q='
    response = requests.get(url + search_name, headers=UA)
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        grades = soup.find('span', class_='classes_dop').text.split()[0]
    except:
        print(f'{search_name} - хуета')
        return
    min_grade = max(int(grades.split('–')[0]), 9)
    max_grade = min_grade
    if len(grades.split('-')) > 1:
        max_grade = int(grades.split('–')[1])
    event.min_grade = min_grade
    event.max_grade = max_grade
    event.save()


if __name__ == '__main__':
    get_olymps_from_rsosh()
