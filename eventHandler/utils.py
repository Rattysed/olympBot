from bs4 import BeautifulSoup
import requests
from eventHandler.models import *

UA = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML,'
                  ' like Gecko) Chrome/99.0.4844.51 Safari/537.36'
}

BAN_WORDS = ['литература', 'дизайн', 'искусство', 'китайск',
             'политология', 'экология', 'психология', 'религиоведение',
             'рисунок', 'композиция', 'философия', 'филология', 'востоковедение',
             'музык', 'сольфеджио', 'дирижирование', 'генетика', 'культур', 'юриспруденц',
             'теология', 'педагог', 'журналистика']


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


if __name__ == '__main__':
    get_olymps_from_rsosh()
