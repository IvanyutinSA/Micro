import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.models.sqlalchemy_models import Base


load_dotenv()

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")

database_url = "postgresql://{}:{}@{}:{}/{}".format(
        POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST,
        POSTGRES_PORT, POSTGRES_DB)
engine = create_engine(database_url, echo=False)
Base.metadata.create_all(engine)


def get_engine():
    return engine


def recreate_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
