import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / '.env')
BASE_IP = os.getenv('BASE_IP')
BASE_PORT = os.getenv('BASE_PORT')
AI_IP = os.getenv('AI_IP')
AI_PORT = os.getenv('AI_PORT')
AN_IP = os.getenv('AN_IP')
AN_PORT = os.getenv('AN_PORT')
