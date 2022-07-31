from django.contrib import admin
from .models import Subjects, Events
# Логин: admin
# Пароль: 123  TODO: поменять на более сложный
# email: admin@example.com


class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', )


class EventsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'notify_date', 'period', 'level', 'subject', 'description')
    search_fields = ('name', )


admin.site.register(Subjects, SubjectsAdmin)
admin.site.register(Events, EventsAdmin)