import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / '.env')
AI_IP = os.getenv('AI_IP')
AI_PORT = int(os.getenv('AI_PORT'))
