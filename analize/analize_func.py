import io
import json
from ServerP import ControlClass


class AnalizeControl(ControlClass):
    def __init__(self, camera):
        self.camera = json.loads(camera)
        response = self.request_get_from_base(
            f'{self.camera["baseserverlink"]}caminfo/{self.camera["camera_id"]}/',
            'Error get caminfo!'
        )
        self.camerainfo = json.loads(json.loads(response.content)['camerainfo'])
        print('Результат init:', self.camerainfo)

    def action(self, data, raw_data, client_socket):
        self.data = json.loads(data)
        camera_id = self.data['camera_id']
        if camera_id == self.camera['camera_id']:
            file_name, file_size, car_boxes = self.data['file_name'], self.data['file_size'], self.data['car_boxes']
            self.file = self.get_file_client_socket(raw_data, client_socket, file_name)
            frame = self.frame_from_buffer_file(self.file)

            # TODO:
            # Анализ парковочных мест в соответствии с car_boxes, парковочными зонами и перспективой
            # POST запрос на drfbase для записи парковочных мест

            self.file = self.buffer_file_from_frame(frame, file_name)
            self.request_to_base(f'{self.camera["baseserverlink"]}api/cameras/{self.camera["camera_id"]}/',
                                 {'file_name': file_name},
                                 {'picture': self.file},
                                 'Send to drfbase:')
            print('Результат action:', self.data)
        else:
            print('Error action! Id not equal!')

    def destroy(self):
        pass
