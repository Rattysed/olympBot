from django.shortcuts import render, HttpResponseRedirect
from .forms import EventForm
from .models import Subjects, Events, Profiles


def test(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/admin")
    class_choices = ((1, 11), (1, 10), (1, 9), (1, 8))
    eventForm = EventForm()
    eventForm.fields['grades'].choices = class_choices

    subjects = Subjects.objects.all()
    subject_choices = []
    for i, sub in enumerate(subjects):
        subject_choices.append((i, sub))
    eventForm.fields['subject'].choices = (tuple(subject_choices))

    profiles = Profiles.objects.all()
    profile_choices = []
    for i, prof in enumerate(profiles):
        profile_choices.append((i, prof))
    eventForm.fields['profile'].choices = (tuple(profile_choices))

    events = Events.objects.exclude(event_priority=0)
    event_choices = []
    for i, ev in enumerate(events):
        event_choices.append((i, ev))
    eventForm.fields['nextEvent'].choices = tuple(event_choices)

    return render(request, 'test.html', {'form': eventForm})
