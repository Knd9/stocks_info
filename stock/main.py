import logging
import logging.config

from fastapi import (
    FastAPI,
)

from db.session import engine
from db.session import Base

# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)


def create_tables():
	Base.metadata.create_all(bind=engine)

def start_application():
    app = FastAPI()
    create_tables()

    return app

app = start_application()
