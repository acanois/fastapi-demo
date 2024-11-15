import os

from dotenv import load_dotenv
load_dotenv()

FAKE_SECRET_KEY = os.environ["FAKE_SECRET_KEY"]
EXPIRE_TIME_MINUTES = os.environ["EXPIRE_TIME_MINUTES"]
