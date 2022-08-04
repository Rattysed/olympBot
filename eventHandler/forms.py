from django import forms


class EventForm(forms.Form):
    name = forms.CharField(label='Название олимпиады')
    notify_date = forms.DateField(label='Дата напоминалки')
    grades = forms.ChoiceField(label='Выберите класс', widget=forms.CheckboxSelectMultiple)
    period = forms.CharField(label='Сраки проведения')
    eventLevel = forms.ChoiceField(label='Уровень олимпиады', choices=((1, 1), (2, 2), (3, 3)))
    priority = forms.IntegerField(label='Отборочность олимпиады', min_value=0, max_value=3)
    subject = forms.MultipleChoiceField(label='Предмет олимпиады')
    profile = forms.MultipleChoiceField(label='Профиль олимпиады')
    nextEvent = forms.ChoiceField(label='Следующий этап олимпиады')
    description = forms.CharField(label='Описание', widget=forms.Textarea)
