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
            file_name = self.data['file_name']
            self.file = self.get_file_client_socket(raw_data, client_socket, file_name)
            frame = self.frame_from_buffer_file(self.file)

            # TODO:
            # Yolo анализ парковочных мест, на вход подается file (io.BytesIO)
            # Выход это пересчитанное значение координат прямоугольников

            self.file = self.buffer_file_from_frame(frame, file_name)
            data = {'camera_id': self.data['camera_id'],
                    'file_name': file_name,
                    'file_size': self.file.__sizeof__(),
                    'car_boxes': [[10, 10, 20, 20], [30, 30, 40, 40], [50, 50, 60, 60]]}
            self.request_to_srv(self.anserver['ip'],
                                self.anserver['port'],
                                '/action/',
                                data,
                                self.file)
            print('Результат action:', self.camera)
        else:
            print('Error action! Id not equal!')

    def destroy(self):
        pass
