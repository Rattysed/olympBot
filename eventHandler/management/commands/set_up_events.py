from django.conf import settings

from django.core.management.base import BaseCommand
from eventHandler.utils import *


class Command(BaseCommand):
    help = "Сосёт олимпиады. Или просто сосёт."

    def handle(self, *args, **options):
        suck_from_olimpiada_sru()
