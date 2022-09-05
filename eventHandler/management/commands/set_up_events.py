from django.conf import settings

from django.core.management.base import BaseCommand
from eventHandler.utils import *


class Command(BaseCommand):
    help = "Единоразовое обновление олимпиад"

    def handle(self, *args, **options):
        # get_from_olimiada_ru()
        add_rawevents_data()
