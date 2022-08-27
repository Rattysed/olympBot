from django.conf import settings

from django.core.management.base import BaseCommand
from eventHandler.utils import *


class Command(BaseCommand):
    help = "Сосёт олимпиады. Или просто сосёт."

    def handle(self, *args, **options):
        # get_olymps_from_rsosh()
        print('События успешно забраны с сайта РСОШ')
        for i, ev in enumerate(RawEvent.objects.all()):
            print(f'Сейчас работаем с ивентом id={i}. Осталось всего-ничего')
            find_grades_of_event(ev)
        print('Мы ёбнутые и мы это сделали!')
