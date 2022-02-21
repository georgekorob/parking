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

    def action(self, data, *args):
        data = json.loads(data)
        camera_id, car_boxes, file_name, file_size = data.values()

        # TODO:
        # Анализ парковочных мест в соответствии с car_boxes, парковочными зонами и перспективой
        # POST запрос на drfbase для записи парковочных мест

        print('Результат action:', data)

    def destroy(self):
        pass
