from django.contrib import admin
from .models import Subjects, Events, User, Profiles


# Логин: admin
# Пароль: 123  TODO: поменять на более сложный
# email: admin@example.com


class SubjectsAndProfilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class EventsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'notify_date', 'period', 'level', 'description')
    search_fields = ('name',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'vk_id', 'tg_id', 'is_rassylka', 'is_subscription', 'end_of_subscription')
    search_fields = ('vk_id', 'tg_id')


admin.site.register(Subjects, SubjectsAndProfilesAdmin)
admin.site.register(Profiles, SubjectsAndProfilesAdmin)
admin.site.register(Events, EventsAdmin)
admin.site.register(User, UserAdmin)
