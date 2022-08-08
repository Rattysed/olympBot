from django import forms
from .models import Subject, Event, Profile




class DateInput(forms.DateInput):
    input_type = 'date'


class EventForm(forms.Form):
    blank_choice = (('', '--- Выберите значение ---'),)
    EVENT_CHOICES = blank_choice + tuple((x.id, x.name) for x in Event.objects.exclude(event_priority=0))
    SUBJECT_CHOICES = ((x.id, x.name) for x in Subject.objects.all())
    PROFILE_CHOICES = ((x.id, x.name) for x in Profile.objects.all())
    name = forms.CharField(label='Название олимпиады', widget=forms.TextInput(attrs={'size':80}))
    notify_date = forms.DateField(label='Дата напоминалки', widget=DateInput)
    grades = forms.MultipleChoiceField(label='Выберите класс', widget=forms.CheckboxSelectMultiple,
                                       choices=((11, 11), (10, 10), (9, 9), (8, 8)))
    period = forms.CharField(label='Сраки проведения')
    event_level = forms.ChoiceField(label='Уровень олимпиады', choices=((1, 1), (2, 2), (3, 3)))
    priority = forms.IntegerField(label='Отборочность олимпиады', min_value=0, max_value=3)
    subject = forms.MultipleChoiceField(label='Предмет олимпиады', choices=SUBJECT_CHOICES)
    profile = forms.MultipleChoiceField(label='Профиль олимпиады', choices=PROFILE_CHOICES)
    next_event = forms.ChoiceField(label='Следующий этап олимпиады', required=False, choices=EVENT_CHOICES)
    event_url = forms.URLField(label='Ссылка на ивент', required=False)
    description = forms.CharField(label='Описание', widget=forms.Textarea, required=False)
