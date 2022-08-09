from django.contrib import admin
from .models import Subject, Event, User, Profile, Question


# Логин: admin
# Пароль: 123  TODO: поменять на более сложный
# email: admin@example.com


class SubjectAndProfileAndQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'notify_date', 'period', 'level', 'event_url', 'description')
    search_fields = ('name',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'vk_id', 'tg_id', 'is_rassylka', 'is_subscription', 'end_of_subscription')
    search_fields = ('vk_id', 'tg_id')


admin.site.register(Subject, SubjectAndProfileAndQuestionAdmin)
admin.site.register(Profile, SubjectAndProfileAndQuestionAdmin)
admin.site.register(Question, SubjectAndProfileAndQuestionAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(User, UserAdmin)
