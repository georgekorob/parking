import datetime, time, requests, cv2, os
from pathlib import Path

cam_server_id = 1
base_addr_ip = '127.0.0.1'
base_addr_port = '8000'
base_api = f'http://{base_addr_ip}:{base_addr_port}/api/cameras/'


class Camera:
    def __init__(self, shotspath, cam):
        self.id = cam.get('id')
        self.ip = cam.get('ip_addr')
        self.port = cam.get('port')
        self.slug_after = cam.get('slug_after')
        self.user = cam.get('username')
        self.password = cam.get('password')
        self.path_to_save = shotspath / f'{self.id:03}'
        if not os.path.exists(self.path_to_save):
            os.mkdir(self.path_to_save)
        self.url = f'rtsp://{self.user}:{self.password}@{self.ip}:{self.port}/{self.slug_after}'
        self.cap = cv2.VideoCapture()
        self.cap.open(self.url)
        self.ms_now = time.time()


def send_picture(cam, frame, namefile, server):
    return requests.patch(f'{server}{cam.id}/',
                          files={'picture': open(namefile, 'rb')},
                          data={'file_name': namefile.name})


shotspath = Path(__file__).resolve().parent.parent / 'camerashots'
if not os.path.exists(shotspath):
    os.mkdir(shotspath)

url = f"{base_api}?cam_server_id={cam_server_id}"
response = requests.get(url)
cams = []
if response:
    cameras = response.json()
    for camera in cameras:
        cams.append(Camera(shotspath, camera))
else:
    raise response.raise_for_status()

try:
    while (True):
        for cam in cams:
            _, frame = cam.cap.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if time.time() - cam.ms_now > 2:
                cam.ms_now = time.time()
                namefile = cam.path_to_save / f'{cam.id:05}.jpg'
                cv2.imwrite(namefile.as_posix(), frame)
                send_picture(cam, frame, namefile, base_api)
                # cv2.imshow('frame', frame)
except Exception as e:
    print(e)
finally:
    for cam in cams:
        cam.cap.release()
    # cv2.destroyAllWindows()
