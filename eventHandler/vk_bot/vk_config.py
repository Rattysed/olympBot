QUESTS = {
    'what_grade': 'В каком классе ты учишься?',
    'main_menu': 'Главное меню',
    'notification_menu': 'Управление уведомлениями - меню',
    'add_olymp': 'Добавление олимпиад к соответствующему предмету',
    'remove_olymp': 'Удаление олимпиады',
    'toggle_event': 'Изменить статус рассылки ивентов',
    'remove_event': 'Удалить ивент из рассылки',
    'warning_grades': 'Предупреждение о сбросе рассылки',
}

COMMAND_ROLLBACK = [
    {'current_question': 'what_grade', 'rollback_command': False, 'rollback_question': False},
    {'current_question': 'main_menu', 'rollback_command': False, 'rollback_question': False},
    {'current_question': 'notification_menu', 'rollback_command': False, 'rollback_question': False},
    {'current_question': 'add_olymp', 'rollback_command': 'меню уведомлений',
     'rollback_question': 'notification_menu'},

    {'current_question': 'remove_olymp', 'rollback_command': 'меню уведомлений',
     'rollback_question': 'notification_menu'},

    {'current_question': 'toggle_event', 'rollback_command': 'изменить уведомления по предметам',
     'rollback_question': 'add_olymp'},

    {'current_question': 'remove_event', 'rollback_command': 'изменить уведомления по предметам',
     'rollback_question': 'remove_olymp'},

    {'current_question': 'warning_grades', 'rollback_command': 'меню уведомлений',
     'rollback_question': 'notification_menu'},
]

USERS = [
    {'username': 'admin', 'password': '123'},
]
