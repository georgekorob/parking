import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / '.env')
CAM_IP = os.getenv('CAM_IP')
CAM_USER = os.getenv('CAM_USER')
CAM_PASSWD = os.getenv('CAM_PASSWD')
