import os



def run_server(state=0):
    if state:
        os.system('python manage.py makemigrations')
        os.system('python manage.py migrate')
    os.system('python manage.py runserver')


if __name__ == '__main__':
    state = input('Выполнить миграции? Y/N').lower()
    if state == 'y':
        state = 1
    else:
        state = 0
    run_server(state)