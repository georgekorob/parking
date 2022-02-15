import datetime, time, requests, cv2, os
from pathlib import Path
from settings import BASE_IP, BASE_PORT, AI_IP, AI_PORT

cam_server_id = 1
base_api = f'http://{BASE_IP}:{BASE_PORT}/api/cameras/'


class Camera:
    def __init__(self, shotspath, cam):
        self.id = cam.get('id')
        self.url = cam.get('url')
        self.path_to_save = shotspath / f'{self.id:03}'
        if not os.path.exists(self.path_to_save):
            os.mkdir(self.path_to_save)
        self.cap = cv2.VideoCapture()
        self.cap.open(self.url)
        self.ms_now = time.time()
        # self.ip = cam.get('ip_addr')
        # self.port = cam.get('port')
        # self.slug_after = cam.get('slug_after')
        # self.user = cam.get('username')
        # self.password = cam.get('password')
        # self.url = f'rtsp://{self.user}:{self.password}@{self.ip}:{self.port}/{self.slug_after}'


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
                file = open(namefile, 'rb')
                name = namefile.name
                requests.patch(url=f'{base_api}{cam.id}/', files={'picture': file}, data={'file_name': name})
                url = f'http://{BASE_IP}:{AI_PORT}/'
                requests.put(url=url, files={'picture': file}, data={'file_name': name})
                # cv2.imshow('frame', frame)
except Exception as e:
    print(e)
finally:
    for cam in cams:
        cam.cap.release()
    # cv2.destroyAllWindows()
