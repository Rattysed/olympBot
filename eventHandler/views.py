from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import EventForm
from django.db.models.query import QuerySet
from .models import Subjects, Events, Profiles


def test(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin")

    if request.method == 'POST':
        eventForm = EventForm(request.POST)
        if eventForm.is_valid():


            pass
        else:

            return HttpResponse(eventForm.errors)
            pass

    eventForm = EventForm()

    return render(request, 'test.html', {'form': eventForm})
