from django.contrib import admin
from .models import *


# Логин: admin
# Пароль: 123  TODO: поменять на более сложный
# email: admin@example.com

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_name', 'full_name')
    search_fields = ('name', 'short_name',)


@admin.register(Subject, Profile)
class ProfileSubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'notify_date', 'period', 'level', 'url', 'description')
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'vk_id', 'tg_id', 'is_rassylka', 'is_subscription', 'end_of_subscription', 'chosen_option')
    search_fields = ('vk_id', 'tg_id')


@admin.register(SubEvent)
class SubEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'grade', 'period', 'org_type')
    search_fields = ('id', 'name')


@admin.register(RawEvent)
class RawEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'level', 'url')
