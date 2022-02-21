import cv2

from ipcams.settings import CAM_IP, CAM_USER, CAM_PASSWD

cap = cv2.VideoCapture()
cap.open(f'rtsp://{CAM_USER}:{CAM_PASSWD}@{CAM_IP}:554/av0_1')
while (True):
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
