import psycopg2
from psycopg2.extensions import cursor as Cursor
from dotenv import load_dotenv
from src.extra import CMD, force_cursor, fetch_adjust
import os


load_dotenv()


class ArticleModel:
    def __init__(self):
        USER = os.environ.get("ARTICLE_DB_USER")
        PASSWORD = os.environ.get("ARTICLE_DB_PASSWORD")
        DB = os.environ.get("ARTICLE_DB_DB")
        HOST = os.environ.get("ARTICLE_DB_HOST")
        PORT = os.environ.get("ARTICLE_DB_PORT")
        db_params = {"host": HOST,
                     "port": PORT,
                     "database": DB,
                     "user": USER,
                     "password": PASSWORD}
        con = psycopg2.connect(**db_params)
        con.autocommit = False
        self.con = con

    @fetch_adjust(return_single=True)
    @force_cursor
    def get_article_title(self, article_id: int, cur: Cursor):
        args = {"article_id": article_id}
        cmd = CMD()
        cmd.append("select")
        cmd.append("title")
        cmd.append("from articles")
        cmd.append("where id = %(article_id)s")
        cmd.append(";")
        cur.execute(cmd.get(), args)
        return cur.fetchall()


class UserModel:
    def __init__(self):
        USER = os.environ.get("USER_DB_USER")
        PASSWORD = os.environ.get("USER_DB_PASSWORD")
        DB = os.environ.get("USER_DB_DB")
        HOST = os.environ.get("USER_DB_HOST")
        PORT = os.environ.get("USER_DB_PORT")
        db_params = {"host": HOST,
                     "port": PORT,
                     "database": DB,
                     "user": USER,
                     "password": PASSWORD}
        con = psycopg2.connect(**db_params)
        con.autocommit = False
        self.con = con

    @fetch_adjust()
    @force_cursor
    def get_users(self, cur: Cursor):
        cmd = CMD()
        cmd.append("select username from users;")
        cur.execute(cmd.get())
        return cur.fetchall()

    @fetch_adjust()
    @force_cursor
    def get_subs(self, author_id: int, cur: Cursor):
        args = {"author_id": author_id}
        cmd = CMD()
        cmd.append("select subscriber_id")
        cmd.append("from subscribers")
        cmd.append("where")
        cmd.append("subscribers.author_id = %(author_id)s")
        cmd.append(";")
        cur.execute(cmd.get(), args)
        return cur.fetchall()

    @fetch_adjust(return_single=True)
    @force_cursor
    def get_subkey(self, user_id: int, cur: Cursor):
        args = {"user_id": user_id}
        cmd = CMD()
        cmd.append("select subscription_key")
        cmd.append("from users")
        cmd.append("where")
        cmd.append("users.id = %(user_id)s")
        cmd.append(";")
        cur.execute(cmd.get(), args)
        return cur.fetchall()
