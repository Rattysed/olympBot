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

    description = models.TextField('Доп. Информация', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'События'
        verbose_name_plural = 'События'
        ordering = ['level']
