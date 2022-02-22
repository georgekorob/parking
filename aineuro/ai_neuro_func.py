import io
import json
import os
from ServerP import ControlClass
from aineuro.yolo import detect


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

            # frame = self.frame_from_buffer_file(self.file)
            # TODO:
            # Yolo анализ парковочных мест, на вход подается file (io.BytesIO)
            # Выход это пересчитанное значение координат прямоугольников
            self.file, car_boxes = self.get_file_from_ai(file_name, self.file)
            # self.file = self.buffer_file_from_frame(frame, file_name)

            data = {'camera_id': self.data['camera_id'],
                    'file_name': file_name,
                    'file_size': self.file.__sizeof__(),
                    'car_boxes': car_boxes}
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

    def get_file_from_ai(self, file_name, file_orig=None):
        if not file_orig:
            with open(file_name, 'rb') as f:
                file_orig = io.BytesIO(f.read())
        test_file_name = '../aineuro/images/temp.jpg'
        with open(test_file_name, 'wb') as f:
            f.write(file_orig.read())
        name_file_result = '../aineuro/exp/temp.jpg'
        if os.path.exists(name_file_result):
            os.remove(name_file_result)
        name_file_result_txt = '../aineuro/exp/labels/temp.txt'
        if os.path.exists(name_file_result_txt):
            os.remove(name_file_result_txt)

        # detect.run
        detect.run(
            weights='../aineuro/yolo/s-512.pt',
            imgsz=(1920, 1080),
            conf_thres=0.25,
            source=test_file_name,
            classes=(0,),
            project='../aineuro',
            exist_ok=True,
            line_thickness=1,
            hide_labels=True,
            save_txt=True
        )

        # path = os.listdir('/detect')
        with open(name_file_result_txt, 'rb') as file:
            labels = [[float(l) for l in lab.decode('utf-8').split(' ')[1:]] for lab in file.read().split(b'\r\n') if lab]
        xl, yl = 1920, 1080
        labels = [[(box[0]-box[2]/2)*xl, (box[1]-box[3]/2)*yl, (box[0]+box[2]/2)*xl, (box[1]+box[3]/2)*yl] for box in labels]
        labels = [[int(b) for b in box] for box in labels]
        with open(name_file_result, 'rb') as f:
            file = io.BytesIO(f.read())
        file.seek(0)
        file.name = file_name
        return file, labels


if __name__ == '__main__':
    control = AINeuroControl('{"camera_id": 1}')
    control.get_file_from_ai('../camerashots/001/frame.jpg')
