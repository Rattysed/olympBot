from django.db import models


class Subjects(models.Model):  # предметы
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предметы'
        verbose_name_plural = 'Предметы'
        ordering = ['name']


class Profiles(models.Model):  # предметы
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['name']


class Events(models.Model):  # События
    name = models.CharField('Название', max_length=100)
    notify_date = models.DateField('Дата напоминания', blank=True)
    period = models.CharField('Сроки проведения', max_length=50)
    level = models.PositiveSmallIntegerField(
        'Уровень олимпиады', default=2, help_text='Значение от 1 до 3'
    )
    event_priority = models.IntegerField('Насколько это событие отборочное', null=True)
    subject = models.ManyToManyField(Subjects, blank=True)
    profile = models.ManyToManyField(Profiles, blank=True)
    event_grade = models.IntegerField('Класс олимпиады', null=True)
    next_event_id = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    description = models.TextField('Доп. Информация', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'События'
        verbose_name_plural = 'События'
        ordering = ['level']


class User(models.Model):
    vk_id = models.CharField('ВКонтакте', max_length=20, blank=True)
    tg_id = models.CharField('Телеграм', max_length=50, blank=True)
    is_rassylka = models.BooleanField('Рассылка', default=False)
    is_subscription = models.BooleanField('Подписка', default=False)
    end_of_subscription = models.DateField('Дата окончания подписки')
    events = models.ManyToManyField(Events)

    def __str__(self):
        return f"{self.vk_id} - {self.tg_id}"

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
