import datetime, time, requests, cv2, io, json


class Camera:
    def __init__(self, cam):
        self.id = cam.get('id')
        self.url = cam.get('camlink')
        self.baseserverlink = cam.get('baseserverlink')
        aiserver = cam.get('aiserverinfo')
        self.aiserver = {
            'id': cam.get('aiserver'),
            'name': aiserver.get('servername'),
            'link': f'http://{aiserver.get("ip")}:{aiserver.get("port")}/'
        }
        anserver = cam.get('anserverinfo')
        self.anserver = {
            'id': cam.get('anserver'),
            'name': anserver.get('servername'),
            'link': f'http://{anserver.get("ip")}:{anserver.get("port")}/'
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


def request_to_srv(url, files=None, data=None, errfstr='', *args):
    try:
        response = requests.put(url=url, files=files, data=data)
        print(response.status_code, response.content)
    except Exception as e:
        print(errfstr.format(*args), end='')
        print(e)


class IPCameraControl:
    cameras = []

    def __init__(self, cam_list_json):
        cam_list = json.loads(cam_list_json)
        self.cameras = [Camera(camera) for camera in cam_list]
        aiserver_links = self.get_ai_servers()
        for aiserver, cameras in aiserver_links.items():
            cameras_bytes = json.dumps([camera.get_json() for camera in cameras])
            request_to_srv(f'{aiserver}init/', None, cameras_bytes,
                           'Send to ai {}:', cameras[0].aiserver["id"])
        print('Результат init:', self.cameras)

    def get_ai_servers(self):
        aiserver_links = {}
        for camera in self.cameras:
            link = camera.aiserver['link']
            if aiserver_links.get(link):
                aiserver_links[link] += [camera]
            else:
                aiserver_links[link] = [camera]
        return aiserver_links

    @staticmethod
    def buffer_file_from_frame(frame_to_buf, filename):
        io_buf_bytes = io.BytesIO(cv2.imencode('.jpg', frame_to_buf)[1].tobytes())
        io_buf_bytes.name = filename
        return io.BufferedReader(io_buf_bytes)

    def shoot(self, id_cameras_json):
        id_cameras = json.loads(id_cameras_json)
        cameras = [camera for camera in self.cameras if camera.id in id_cameras]
        for camera in cameras:
            _, frame = camera.cap.read()
            namefile = f'{camera.id:05}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}.jpeg'
            io_buf_file = self.buffer_file_from_frame(frame, namefile)
            request_to_srv(f'{camera.baseserverlink}api/cameras/{camera.id}/',
                           {'picture': io_buf_file}, {'file_name': namefile},
                           'Send to drfbase:')
            request_to_srv(f'{camera.aiserver["link"]}calc/',
                           {'picture': io_buf_file}, {'file_name': namefile, 'camera_id': camera.id},
                           'Send to ai {}:', camera.aiserver["id"])
            # try:
            #     response = requests.patch(url=f'{camera.baseserverlink}api/cameras/1/',
            #                               files={'picture': io_buf_file},
            #                               data={'file_name': namefile})
            #     print(response.status_code, response.content)
            # except Exception as e:
            #     print('Send to drfbase:', e)
            # try:
            #     response = requests.put(url=f'{camera.aiserver["link"]}calc/',
            #                             files={'picture': io_buf_file},
            #                             data={'file_name': namefile})
            #     print(response.status_code, response.content)
            # except Exception as e:
            #     print('Send to ai:', e)

    def destroy(self):
        for camera in self.cameras:
            camera.cap.release()
