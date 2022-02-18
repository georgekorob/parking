import datetime, time, requests, cv2, os
import io
from pathlib import Path
from settings import BASE_IP, BASE_PORT, AI_IP, AI_PORT

cam_server_id = 1
base_api = f'http://{BASE_IP}:{BASE_PORT}/api/cameras/'

import numpy as np
import urllib.request

# url = 'http://www.pyimagesearch.com/wp-content/uploads/2015/01/google_logo.png'
# resp = urllib.request.urlopen(url)
# image = resp.read()
# image = np.asarray(bytearray(image), dtype="uint8")
# image = cv2.imdecode(image, cv2.IMREAD_COLOR)
# data_encode = np.array(image)
# cv2.imshow('URL2Image', image)
# cv2.waitKey()

class Camera:
    def __init__(self, shotspath, cam):
        self.id = cam.get('id')
        self.url = cam.get('camlink')
        aiserver = cam.get('aiserverinfo')
        self.aiserverlink = f'http://{aiserver.get("ip")}:{aiserver.get("port")}/'
        self.path_to_save = shotspath / f'{self.id:03}'
        if not os.path.exists(self.path_to_save):
            os.mkdir(self.path_to_save)
        self.cap = cv2.VideoCapture()
        self.cap.open(self.url)
        self.ms_now = time.time()


shotspath = Path(__file__).resolve().parent.parent / 'camerashots'
if not os.path.exists(shotspath):
    os.mkdir(shotspath)

url = f"{base_api}?camserver={cam_server_id}"
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
                namefile = f'{cam.id:05}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}.jpg'
                namepathfile = cam.path_to_save / namefile
                cv2.imwrite(namepathfile.as_posix(), frame)
                file = open(namepathfile, 'rb')
                jpeg_frame = cv2.imencode('.jpg', frame)[1].tobytes()
                jpeg_frame = io.BytesIO(jpeg_frame)
                requests.patch(url=f'{base_api}{cam.id}/', files={'picture': file}, data={'file_name': namefile})
                url = f'http://{BASE_IP}:{AI_PORT}/'
                # requests.put(url=url, files={'picture': file}, data={'file_name': name})
                # cv2.imshow('frame', frame)
except Exception as e:
    print(e)
finally:
    for cam in cams:
        cam.cap.release()
    # cv2.destroyAllWindows()
