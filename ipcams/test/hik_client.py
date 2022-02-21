from hikvisionapi import Client
import cv2
from ipcams.settings import CAM_USER, CAM_PASSWD, CAM_IP

try:
    cam = Client(f'http://{CAM_IP}', CAM_USER, CAM_PASSWD, timeout=30)
    cam.count_events = 2  # The number of events we want to retrieve (default = 1)
    while (True):
        response = cam.Streaming.channels[102].picture(method='get', type='opaque_data')
        with open('screen.jpg', 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        img = cv2.imread('screen.jpg')
        cv2.imshow("show", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except Exception as e:
    print('Error!!! Client', e)
