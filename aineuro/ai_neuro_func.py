import io
import json

from ServerP import ControlClass


class AINeuroControl(ControlClass):
    def __init__(self, camera):
        self.camera = json.loads(camera)
        self.anserver = self.camera['anserver']
        self.request_to_srv(self.anserver['ip'],
                            self.anserver['port'],
                            '/init/',
                            self.camera)
        print('Результат init:', self.camera)

    def action(self, data, raw_data, client_socket):
        self.data = json.loads(data)
        if self.data['camera_id'] == self.camera['camera_id']:
            self.file = io.BytesIO()
            # file_for_save = open(f'{self.data["file_name"]}', 'wb')
            self.file.write(raw_data)
            while True:
                line = client_socket.recv(1024)  # получаем байтовые строки
                self.file.write(line)  # пишем байтовые строки в файл на сервере
                if not line:
                    break
            self.file.seek(0)

            # TODO:
            # Yolo анализ парковочных мест, на вход подается file (io.BytesIO)
            # Выход это пересчитанное значение координат прямоугольников

            data = {'camera_id': self.data['camera_id'],
                    'file_name': self.data['file_name'],
                    'file_size': self.file.__sizeof__(),
                    'car_boxes': [[10, 10, 20, 20], [30, 30, 40, 40], [50, 50, 60, 60]]}
            self.request_to_srv(self.anserver['ip'],
                                self.anserver['port'],
                                '/action/',
                                data)
            print('Результат action:', self.camera)
        else:
            print('Error action! Id not equal!')

    def destroy(self):
        pass

# def get_an_servers(self, ai_camera):
#     anserver_links = {}
#     for camera in ai_camera:
#         link = camera['anserver']['link']
#         if anserver_links.get(link):
#             anserver_links[link] += [camera]
#         else:
#             anserver_links[link] = [camera]
#     return anserver_links
