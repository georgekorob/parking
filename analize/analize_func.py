import json
from ServerP import ControlClass


class AnalizeControl(ControlClass):
    def __init__(self, camera):
        self.camera = json.loads(camera)

        # TODO:
        # GET запрос на сервер за информацией о камере, парковочных зонах и перспективе

        print('Результат init:', self.camera)

    def action(self, data, *args):
        data = json.loads(data)
        camera_id, car_boxes, file_name, file_size = data.values()

        # TODO:
        # Анализ парковочных мест в соответствии с car_boxes, парковочными зонами и перспективой
        # POST запрос на drfbase для записи парковочных мест

        print(data)

    def destroy(self):
        pass
