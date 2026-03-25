from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()


celery = Celery(broker=os.getenv("REDIS_URL"))


def test_shit():
    celery.send_task("notify_followers", args=[1, 1])
