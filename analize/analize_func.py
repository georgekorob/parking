import json, requests


def request_to_srv(url, data, errfstr, *args):
    try:
        response = requests.put(url=url, data=data)
        print(response.status_code, response.content)
    except Exception as e:
        print(errfstr.format(*args, e))


class AnalizeControl:
    def __init__(self):
        self.analize = {}

    def init(self, an_cameras):
        an_cameras = json.loads(an_cameras)
        self.set_analize(an_cameras)
        print('Результат init:', self.analize)

    def set_analize(self, an_cameras):
        for cam in an_cameras:
            cam_id = cam.get('camera_id')
            if self.analize.get(cam_id):
                self.analize[cam_id] += [cam]
            else:
                self.analize[cam_id] = [cam]

    def calc(self, info):
        pass

    def destroy(self):
        pass
