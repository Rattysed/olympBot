import django.utils.timezone
from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import Permission


class Subject(models.Model):  # предметы
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предметы'
        verbose_name_plural = 'Предметы'
        ordering = ['name']


class Profile(models.Model):  # предметы
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['name']


class Event(models.Model):  # События
    name = models.CharField('Название', max_length=100)
    notify_date = models.DateField('Дата напоминания', blank=True, default=django.utils.timezone.now)
    period = models.CharField('Сроки проведения', max_length=50)
    level = models.PositiveSmallIntegerField(
        'Уровень олимпиады', default=2, help_text='Значение от 1 до 3'
    )
    # event_priority = models.IntegerField('Насколько это событие отборочное', null=True)
    subject = models.ManyToManyField(Subject, blank=True)
    profile = models.ForeignKey(Profile, blank=True, on_delete=models.SET_NULL, null=True)
    # event_grade = models.IntegerField('Класс олимпиады', null=True)
    next_event_id = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    url = models.URLField(max_length=160, default='https://')
    description = models.TextField('Доп. Информация', blank=True)
    is_visible = models.BooleanField('Отображение в текущих списках', default=False, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'События'
        verbose_name_plural = 'События'
        ordering = ['level']


class SubEvent(models.Model):
    name = models.CharField('Название', max_length=100)
    main_event = models.ForeignKey(Event, blank=True, null=True, on_delete=models.SET_NULL)
    grade = models.IntegerField('Класс события', blank=True)
    notify_date = models.DateField('Дата напоминания', default=django.utils.timezone.now)
    period = models.CharField('Информация о сраках проведения', max_length=200, default='')
    org_type = models.IntegerField('Дистант или очно', default=0)


class Question(models.Model):
    short_name = models.CharField('Краткое имя', max_length=50, default='blank_question')
    full_name = models.CharField('Название', max_length=150, null=True)

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['id']


class User(models.Model):
    vk_id = models.CharField('ВКонтакте', max_length=20, blank=True)
    tg_id = models.CharField('Телеграм', max_length=50, blank=True)
    is_rassylka = models.BooleanField('Рассылка', default=True)
    grade = models.IntegerField('Класс пользователя', null=True)
    is_subscription = models.BooleanField('Подписка', default=False)
    end_of_subscription = models.DateField('Дата окончания подписки', null=True)
    events = models.ManyToManyField(SubEvent)
    current_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    chosen_option = models.ForeignKey(Subject, on_delete=models.SET_NULL, blank=True, null=True)
    role = models.ForeignKey(DjangoUser, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.vk_id} - {self.tg_id}"

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
