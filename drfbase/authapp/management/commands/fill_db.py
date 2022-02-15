import json
import os
import random
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from authapp.models import User
from camsapp.models import Camera
from srvapp.models import CAMServer, AIServer, ANServer


def load_from_json(file_name):
    try:
        with open(file_name, mode='r', encoding='utf-8') as infile:
            return json.load(infile)
    except UnicodeDecodeError:
        with open(file_name, mode='r', encoding='windows-1251') as infile:
            return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        if os.path.exists('db.sqlite3'):
            os.remove('db.sqlite3')
        print('deleted db.sqlite3')
        for dirapp in os.listdir():
            if os.path.isdir(dirapp) and os.path.exists(f'{dirapp}/migrations'):
                for filemig in os.listdir(f'{dirapp}/migrations'):
                    if filemig not in ['__init__.py', '__pycache__']:
                        filename = f'{dirapp}/migrations/{filemig}'
                        os.remove(filename)
                        print(f'deleted {filename}')
        print('makemigrations...')
        call_command('makemigrations')
        print('migrate...')
        call_command('migrate')
        # print('User.objects.all().delete()...')
        # print('Camera.objects.all().delete()...')
        # User.objects.all().delete()
        # CAMServer.objects.all().delete()
        # AIServer.objects.all().delete()
        # ANServer.objects.all().delete()
        # Camera.objects.all().delete()
        User.objects.create_superuser(username=os.getenv('SUPER_USER_USERNAME'),
                                      password=os.getenv('SUPER_USER_PASSWORD'),
                                      email=os.getenv('SUPER_USER_EMAIL'))
        User.objects.create_user(username='geekbrains',
                                 password='passfortest',
                                 email='georgekorob@gmail.com')
        camserver = CAMServer.objects.create(name='camserver')
        aiserver = AIServer.objects.create(name='aiserver',
                                           ip_address=os.getenv('AI_IP'),
                                           port=os.getenv('AI_PORT'))
        anserver = ANServer.objects.create(name='anserver')
        # camera = Camera.objects.create(ip_addr=os.getenv('CAM_IP'),
        #                                username=os.getenv('CAM_USER'),
        #                                password=os.getenv('CAM_PASSWD'))
        camera = Camera.objects.create(cam_server=camserver,
                                       ai_server=aiserver,
                                       url=os.getenv('CAM_URL'))
        camera.users.set(User.objects.all())
        print('DONE!!!')

# User.objects.all().delete()
# for name in ['authapp']:
#     filename = f'./{name}/fixtures/{name}.json'
#     call_command('loaddata', filename, app_label=name)
