import os
from dotenv import load_dotenv

load_dotenv()

FAKE_SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
EXPIRE_TIME_MINUTES = os.environ["EXPIRE_TIME_MINUTES"]
