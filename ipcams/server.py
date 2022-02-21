from ip_cam_func import IPCameraControl
from ServerP import ServerIPCam
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / '.env')
IPCAM_IP = os.getenv('IPCAM_IP')
IPCAM_PORT = int(os.getenv('IPCAM_PORT'))
ServerIPCam(IPCameraControl, IPCAM_IP, IPCAM_PORT)
