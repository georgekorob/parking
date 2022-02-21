import datetime, time, cv2, io, json
from ServerP import ControlClass


class Camera:
    def __init__(self, cam):
        self.id = cam.get('id')
        self.url = cam.get('camlink')
        self.baseserverlink = cam.get('baseserverlink')
        aiserver = cam.get('aiserverinfo')
        self.aiserver = {
            'id': cam.get('aiserver'),
            'name': aiserver.get('servername'),
            'ip': aiserver.get('ip'),
            'port': aiserver.get('port')
        }
        anserver = cam.get('anserverinfo')
        self.anserver = {
            'id': cam.get('anserver'),
            'name': anserver.get('servername'),
            'ip': anserver.get('ip'),
            'port': anserver.get('port')
        }
        self.cap = cv2.VideoCapture()
        self.cap.open(self.url)
        self.ms_now = time.time()

    def get_json(self):
        return {
            'camera_id': self.id,
            'baseserverlink': self.baseserverlink,
            'aiserver': self.aiserver,
            'anserver': self.anserver
        }


class IPCameraControl(ControlClass):
    def __init__(self, cam_list_json):
        self.camera = Camera(json.loads(cam_list_json)[0])
        camera_json = self.camera.get_json()
        self.request_to_srv(self.camera.aiserver['ip'],
                            self.camera.aiserver['port'],
                            '/init/',
                            camera_json)
        print('Результат init:', camera_json)

    def action(self, id_cameras_json, *args):
        if self.camera.id == json.loads(id_cameras_json)[0]:
            _, frame = self.camera.cap.read()
            namefile = f'{self.camera.id:05}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}.jpg'
            io_buf_file = self.buffer_file_from_frame(frame, namefile)
            # self.request_to_base(f'{self.camera.baseserverlink}api/cameras/{self.camera.id}/',
            #                      {'file_name': namefile},
            #                      {'picture': io_buf_file},
            #                      'Send to drfbase:')
            self.request_to_srv(self.camera.aiserver['ip'],
                                self.camera.aiserver['port'],
                                '/action/',
                                {'file_name': namefile, 'camera_id': self.camera.id},
                                io_buf_file)
            print('Результат action:', io_buf_file.__sizeof__())
        else:
            print('Error action! Id not equal!')

    def destroy(self):
        self.camera.cap.release()
