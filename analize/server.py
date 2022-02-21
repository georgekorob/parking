from analize_func import AnalizeControl
from ServerP import ServerIPCam
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / '.env')
AN_IP = os.getenv('AN_IP')
AN_PORT = int(os.getenv('AN_PORT'))
ServerIPCam(AnalizeControl, AN_IP, AN_PORT)
