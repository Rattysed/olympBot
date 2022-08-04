from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .forms import EventForm
from .models import Subjects, Events, Profiles


def test(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin")

    if request.method == 'POST':
        eventForm = EventForm(request.POST)
        if eventForm.is_valid():
            print('Fuck yeah')
            return
            pass
        else:
            print(eventForm.errors)
            print('Fuck no')
            return HttpResponse(eventForm.errors)
            pass
    class_choices = (('1', 11), ('2', 10), ('3', 9), ('4', 8))
    eventForm = EventForm()
    eventForm.fields['grades'].choices = class_choices

    subjects = Subjects.objects.all()
    eventForm.fields['subject'].choices = ((x.id, x.name) for x in subjects)

    profiles = Profiles.objects.all()
    eventForm.fields['profile'].choices = ((x.id, x.name) for x in profiles)

    blank_choice = (('', '--- Выберите значение ---'),)
    events = Events.objects.exclude(event_priority=0)
    eventForm.fields['nextEvent'].choices = blank_choice + tuple((x.id, x.name) for x in events)

    return render(request, 'test.html', {'form': eventForm})
