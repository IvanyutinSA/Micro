import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from src.models.sqlalchemy_models import Base


load_dotenv()
database_url = os.environ.get("DATABASE_URL", "")


def get_engine():
    engine = create_engine(database_url, echo=False)

    Base.metadata.create_all(engine)
    return engine
