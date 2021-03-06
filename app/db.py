# Third Party Library
from sqlalchemy import create_engine

# Local Library
from . import config

engine = create_engine(config.DATABASE_URI, future=True, echo=True)
