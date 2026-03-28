from src.extra import generate_headers
import random
from celery import Celery
import requests
import os
from dotenv import load_dotenv
from src.model import ArticleModel, UserModel
import logging

load_dotenv()

PUSH_URL = os.environ.get("PUSH_URL")
ARTICLE_SERVICE_URL = os.environ.get("ARTICLE_SERVICE_URL")
API_KEY = os.environ.get("API_KEY", "NONE")

article_model = ArticleModel()
user_model = UserModel()


celery = Celery("worker", broker=os.getenv("REDIS_URL"))

completed = set()


def to_dlq(task, article_id: int):
    if task.request.retries >= task.max_retries:
        args = [article_id, task.name]
        celery.send_task("dlq.consume", args)


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
        to_dlq(self, article_id)
        raise self.retry(exc=e, countdown=2**self.request.retries)


@celery.task(bind=True, max_retries=5, name="post.moderate")
def post_moderate(self, post_id: int, author_id: int,
                  title: str, body: str, requested_by: int):
    try:
        approved = random.choice([True, False])
        if not approved:
            logging.warning(f"Article: {post_id} rejected")
            headers = generate_headers(API_KEY)
            url = f"{ARTICLE_SERVICE_URL}/articles/{post_id}/reject"
            response = requests.post(url,
                                     json={},
                                     headers=headers)
            response.raise_for_status()
            return
        logging.warning(f"Article: {post_id} approved")
        args = [post_id, title, body, author_id]
        celery.send_task("post.generate_preview", args)
    except Exception as e:
        to_dlq(self, post_id)
        raise self.retry(exc=e, countdown=2**self.request.retries)


@celery.task(bind=True, max_retries=5, name="post.generate_preview")
def generate_preview(self, article_id: int, title: str, body: str,
                     author_id: int):
    try:
        preview_url = "preview_url_{article_id}_{title}_{body}"
        headers = generate_headers(API_KEY)
        url = f"{ARTICLE_SERVICE_URL}/articles/{article_id}/preview"
        json = {"preview_url": preview_url}

        response = requests.put(url, json=json, headers=headers)
        response.raise_for_status()

        logging.warning(f"Preview generated for {article_id}")
        celery.send_task("post.publish", [author_id, article_id])
    except Exception as e:
        to_dlq(self, article_id)
        raise self.retry(exc=e, countdown=2**self.request.retries)


@celery.task(bind=True, max_retries=5, name="post.publish")
def post_publish(self, author_id: int, article_id: int):
    try:
        headers = generate_headers(API_KEY)
        url = f"{ARTICLE_SERVICE_URL}/articles/{article_id}/publish"

        response = requests.put(url, headers=headers)
        response.raise_for_status()

        logging.warning(f"Article {article_id} published")
        celery.send_task("notify_followers", [author_id, article_id])
    except Exception as e:
        to_dlq(self, article_id)
        raise self.retry(exc=e, countdown=2**self.request.retries)


@celery.task(bind=True, max_retries=5, name="dlq.consume")
def dlq_consume(self, article_id: int, source: str):
    try:
        if source == "post.moderate":
            headers = generate_headers(API_KEY)
            url = f"{ARTICLE_SERVICE_URL}/articles/{article_id}/reject"

            response = requests.put(url, headers=headers)
            response.raise_for_status()

            return

        if source == "post.generate_preview":
            headers = generate_headers(API_KEY)
            url = f"{ARTICLE_SERVICE_URL}/articles/{article_id}/error"

            response = requests.put(url, headers=headers)
            response.raise_for_status()

            return

        if source == "post.generate_preview":
            headers = generate_headers(API_KEY)
            url = f"{ARTICLE_SERVICE_URL}/articles/{article_id}/error"

            response = requests.put(url, headers=headers)
            response.raise_for_status()

            return

        logging.warning("Task: {source} happend to be in dlq")

    except Exception as e:
        raise self.retry(exc=e, countdown=2**self.request.retries)
