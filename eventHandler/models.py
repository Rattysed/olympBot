from django.db import models


class Subjects(models.Model):  # предметы
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предметы'
        verbose_name_plural = 'Предметы'
        ordering = ['name']


class Events(models.Model):  # События
    name = models.CharField('Название', max_length=100)
    notify_date = models.DateField('Дата напоминания', blank=True)
    period = models.CharField('Сроки проведения', max_length=50)
    level = models.PositiveSmallIntegerField(
        'Уровень олимпиады', default=2, help_text='Значение от 1 до 3'
    )

    subject = models.ForeignKey(Subjects, on_delete=models.SET_NULL, null=True)
    next_event_id = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    description = models.TextField('Доп. Информация', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'События'
        verbose_name_plural = 'События'
        ordering = ['level']


class User(models.Model):
    vk_id = models.CharField('ВКонтакте', max_length=20)
    tg_id = models.CharField('Телеграм', max_length=50)
    is_rassylka = models.BooleanField('Рассылка', default=False)
    is_subscription = models.BooleanField('Подписка', default=False)
    end_of_subscription = models.DateField('Дата окончания подписки')

    def __str__(self):
        return f"{self.vk_id} - {self.tg_id}"

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'


class OlympsToUser(models.Model):
    event_id = models.ForeignKey(Events, on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.user_id} - {self.event_id}"
