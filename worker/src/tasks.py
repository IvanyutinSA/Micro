from celery import Celery
import requests
import os
from dotenv import load_dotenv
from src.model import ArticleModel, UserModel
from src.test import test_shit
import logging

load_dotenv()

PUSH_URL = os.environ.get("PUSH_URL")

article_model = ArticleModel()
user_model = UserModel()


celery = Celery("worker", broker=os.getenv("REDIS_URL"))

completed = set()


@celery.task(bind=True, max_retries=5, name="notify_followers")
def notify_followers(self, author_id: int, article_id: int):
    try:
        if self.request.id in completed:
            return
        sub_ids = user_model.get_subs(author_id)
        article_title = article_model.get_article_title(article_id)
        article_title = article_title[:10]
        msg = (f"Пользователь {author_id} выпустил новый пост: " +
               f"{article_title}...")
        for sub_id in sub_ids:
            key = user_model.get_subkey(sub_id)
            if not key:
                logging.warning("skip: no key for subscriber=%d", sub_id)
                continue
            print(f"key: {key}\nmsg: {msg}")

            headers = {"Authorization": f"Bearer {key}",
                       "Content-Type": "application/json"}
            json = {"message": msg}
            timeout = 5
            r = requests.post(PUSH_URL,
                              headers=headers,
                              json=json,
                              timeout=timeout)
            r.raise_for_status()
        completed.add(self.request.id)
    except Exception as e:
        raise self.retry(exc=e, countdown=2**self.request.retries)


test_shit()
