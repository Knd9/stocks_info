import os
import sys
sys.path.append("..")

from dotenv import load_dotenv
from pathlib import Path


env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:

    API_TOKEN = os.environ['API_TOKEN']
    POSTGRES_HOST = os.environ['POSTGRES_HOST']
    POSTGRES_PORT = os.environ['POSTGRES_PORT']
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
    POSTGRES_DB = os.environ['POSTGRES_DB']
    DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

    @property
    def db_name(self):
        if os.environ['RUN_ENV'] == 'test':
            return 'test_' + self.POSTGRES_DB

        return self.POSTGRES_DB

settings = Settings()
