from celery import Celery
import os
from dotenv import load_dotenv
from src.model import ArticleModel, UserModel
from src.test import test_shit
from pprint import pprint

load_dotenv()
article_model = ArticleModel()
user_model = UserModel()


celery = Celery("worker", broker=os.getenv("REDIS_URL"))

completed = set()


@celery.task(bind=True, max_retries=3, name="playground")
def playground(self):
    if self.request.id in completed:
        return
    print(self.request.id)
    completed.add(self.request.id)
    raise self.retry(countdown=1)


@celery.task(bind=True, max_retries=1, name="display_articles")
def display_articles(self, name: str):
    try:
        print(article_model.get_article_title(1))
    except Exception as e:
        raise self.retry(exc=e, countdown=2**self.request.retries)


@celery.task(bind=True, max_retries=1, name="get_subs")
def get_subs(self, author_id: int):
    print(user_model.get_subs(author_id))


@celery.task(bind=True, max_retries=1, name="get_subkey")
def get_subkey(self, user_id: int):
    print(user_model.get_subkey(user_id))


@celery.task(bind=True, max_retries=1, name="display_users")
def display_users(self, name: str):
    try:
        print(user_model.get_users())
    except Exception as e:
        raise self.retry(exc=e, countdown=2**self.request.retries)


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
            print(f"key: {key}\nmsg: {msg}")
    except Exception as e:
        raise self.retry(exc=e, countdown=2**self.request.retries)


test_shit()
