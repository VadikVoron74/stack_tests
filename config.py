import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
LOGIN = os.getenv("STACK_LOGIN")
PASSWORD = os.getenv("STACK_PASSWORD")
ADDRESSES_URL = BASE_URL + "accounts"




