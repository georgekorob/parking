import json, requests


def request_to_srv(url, data, errfstr, *args):
    try:
        response = requests.put(url=url, data=data)
        print(response.status_code, response.content)
    except Exception as e:
        print(errfstr.format(*args, e))


class AINeuroControl:
    def __init__(self):
        self.ai_neuros = {}

    def init(self, ai_cameras):
        ai_cameras = json.loads(ai_cameras)
        self.set_ai_neuros(ai_cameras)
        anserver_links = self.get_an_servers(ai_cameras)
        for anserver, cameras in anserver_links.items():
            data_bytes = json.dumps(cameras)
            request_to_srv(f'{anserver}init/',
                           data_bytes,
                           'Send to an {}: {}',
                           cameras[0]["anserver"]["id"])
        print('Результат init:', self.ai_neuros)

    def set_ai_neuros(self, ai_cameras):
        for cam in ai_cameras:
            cam_id = cam.get('camera_id')
            if self.ai_neuros.get(cam_id):
                self.ai_neuros[cam_id] += [cam]
            else:
                self.ai_neuros[cam_id] = [cam]

    def get_an_servers(self, ai_cameras):
        anserver_links = {}
        for camera in ai_cameras:
            link = camera['anserver']['link']
            if anserver_links.get(link):
                anserver_links[link] += [camera]
            else:
                anserver_links[link] = [camera]
        return anserver_links

    def calc(self, client_socket, raw_data):
        file_name = raw_data[12]
        camera_id = int(raw_data[16])
        file_for_save = open(file_name, 'wb')
        while True:
            line = client_socket.recv(1024)  # получаем байтовые строки
            file_for_save.write(line)  # пишем байтовые строки в файл на сервере
            if not line:
                break

    def destroy(self):
        pass
