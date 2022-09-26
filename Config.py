import os
from dotenv import load_dotenv

load_dotenv()

access_token = os.getenv('access_token')
token1 = os.getenv('token1')
DSN = os.getenv('DSN')