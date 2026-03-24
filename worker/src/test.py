from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()


celery = Celery(broker=os.getenv("REDIS_URL"))


def test_shit():
    celery.send_task("playground")
    celery.send_task("display_articles", args=["Mia"])
    celery.send_task("display_users", args=["Mia"])
    celery.send_task("get_subs", args=[1])
    celery.send_task("get_subkey", args=[1])
    celery.send_task("get_subkey", args=[2])
    celery.send_task("notify_followers", args=[1, 1])
