from dotenv import load_dotenv
import os

load_dotenv()

SERVER_ADDRESS = os.getenv('SERVER_ADDRESS')
SERVER_PORT = os.getenv('SERVER_PORT')
POSTGRES_CONN = os.getenv('POSTGRES_CONN')
POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')
APP_DEBUG = bool(os.getenv('APP_DEBUG'))