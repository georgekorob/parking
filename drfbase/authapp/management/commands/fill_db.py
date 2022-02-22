import json
import os
import random
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from authapp.models import User
from camsapp.models import Camera, CameraInfo
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
        camserver = CAMServer.objects.create(servername='camserver',
                                             ip=os.getenv('IPCAM_IP'),
                                             port=os.getenv('IPCAM_PORT'))
        aiserver = AIServer.objects.create(servername='aiserver',
                                           ip=os.getenv('AI_IP'),
                                           port=os.getenv('AI_PORT'))
        anserver = ANServer.objects.create(servername='anserver',
                                           ip=os.getenv('AN_IP'),
                                           port=os.getenv('AN_PORT'))
        camera = Camera.objects.create(camserver=camserver,
                                       aiserver=aiserver,
                                       anserver=anserver,
                                       baseserverlink=f'http://{os.getenv("BASE_IP")}:{os.getenv("BASE_PORT")}/',
                                       camlink=os.getenv('CAM_URL'))
        camera.users.set(User.objects.all())
        camerainfo = {
            'frame_points': [[313, 405],
                             [431, 97],
                             [1401, 43],
                             [1809, 395]],
            'map_points': [[657, 515],
                           [633, 713],
                           [271, 473],
                           [361, 261]],
            'coord_points': [[59.984439, 30.379857],  # Угол дороги
                             [59.984052, 30.379763],  # Левый угол дома
                             [59.984527, 30.378334],  # Правый угол дома
                             [59.984944, 30.378689]],  # Угол правого дома
            'cam_height': 30,
            'parking_lines': [[[914, 858], [1133, 853]], [[1195, 850], [1523, 807]], [[1523, 807], [1784, 727]],
                              [[926, 1022], [1496, 961]]],
        }  # , [[0,0],[0,0]]
        CameraInfo.objects.create(camera=camera, camerainfo=json.dumps(camerainfo))
        print('DONE!!!')

# User.objects.all().delete()
# for name in ['authapp']:
#     filename = f'./{name}/fixtures/{name}.json'
#     call_command('loaddata', filename, app_label=name)
