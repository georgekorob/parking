import datetime, time, requests, cv2, io


class Camera:
    def __init__(self, cam):
        self.id = cam.get('id')
        self.url = cam.get('camlink')
        aiserver = cam.get('aiserverinfo')
        self.aiserverlink = f'http://{aiserver.get("ip")}:{aiserver.get("port")}/'
        self.cap = cv2.VideoCapture()
        self.cap.open(self.url)
        self.ms_now = time.time()


class CameraControl:
    cameras = []

    def __init__(self, cam_json_list):
        self.cameras = [Camera(camera) for camera in cam_json_list]

    @staticmethod
    def buffer_file_from_frame(frame_to_buf, filename):
        io_buf_bytes = io.BytesIO(cv2.imencode('.jpg', frame_to_buf)[1].tobytes())
        io_buf_bytes.name = filename
        return io.BufferedReader(io_buf_bytes)

    def shoot(self, id_cameras):
        cameras = [camera for camera in self.cameras if camera.id in id_cameras]
        for camera in cameras:
            _, frame = camera.cap.read()
            namefile = f'{camera.id:05}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}.jpeg'
            io_buf_file = self.buffer_file_from_frame(frame, namefile)
            try:
                requests.patch(url=f'http://127.0.0.1:8000/api/cameras/1/',
                               files={'picture': io_buf_file},
                               data={'file_name': namefile})
            except Exception as e:
                print('Send to drfbase:', e)
            try:
                requests.put(url=camera.aiserverlink,
                             files={'picture': io_buf_file},
                             data={'file_name': namefile})
            except Exception as e:
                print('Send to ai:', e)

    def destroy(self):
        for camera in self.cameras:
            camera.cap.release()
