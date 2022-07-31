from django.http import HttpResponse
from eventHandler.request_handler import get_all_this_date
from datetime import date

def test(request):
    return HttpResponse(f"<h2>{get_all_this_date(date(2022, 8, 2))[0].name}</h2>")

