from django.contrib import admin
from .models import Subject, Event, User, Profile, Question


# Логин: admin
# Пароль: 123  TODO: поменять на более сложный
# email: admin@example.com


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_name', 'full_name')
    search_fields = ('name', 'short_name',)


class ProfileSubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'notify_date', 'period', 'level', 'url', 'description')
    search_fields = ('name',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'vk_id', 'tg_id', 'is_rassylka', 'is_subscription', 'end_of_subscription', 'chosen_option')
    search_fields = ('vk_id', 'tg_id')


admin.site.register(Subject, ProfileSubjectAdmin)
admin.site.register(Profile, ProfileSubjectAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(User, UserAdmin)
