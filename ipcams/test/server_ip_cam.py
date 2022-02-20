import datetime, time, requests, cv2, os, io
from settings import BASE_IP, BASE_PORT

cam_server_id = 1
base_api = f'http://{BASE_IP}:{BASE_PORT}/api/cameras/'


class Camera:
    def __init__(self, cam):
        self.id = cam.get('id')
        self.url = cam.get('camlink')
        aiserver = cam.get('aiserverinfo')
        self.aiserverlink = f'http://{aiserver.get("ip")}:{aiserver.get("port")}/'
        self.cap = cv2.VideoCapture()
        self.cap.open(self.url)
        self.ms_now = time.time()


def get_cameras(api, server_id):
    response = requests.get(f"{api}?camserver={server_id}")
    if response:
        return [Camera(camera) for camera in response.json()]
    else:
        raise response.raise_for_status()


def buffer_file_from_frame(frame_to_buf, filename):
    io_buf_bytes = io.BytesIO(cv2.imencode('.jpg', frame_to_buf)[1].tobytes())
    io_buf_bytes.name = filename
    return io.BufferedReader(io_buf_bytes)


try:
    cams = get_cameras(base_api, cam_server_id)
    while (True):
        for cam in cams:
            _, frame = cam.cap.read()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if time.time() - cam.ms_now > 2:
                cam.ms_now = time.time()
                namefile = f'{cam.id:05}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}.jpeg'
                io_buf_file = buffer_file_from_frame(frame, namefile)
                requests.patch(url=f'http://127.0.0.1:8000/api/cameras/1/',
                               files={'picture': io_buf_file},
                               data={'file_name': namefile})

                # requests.put(url=cam.aiserverlink, files={'picture': io_buf_file}, data={'file_name': namefile})
except Exception as e:
    print(e)
finally:
    for cam in cams:
        cam.cap.release()
