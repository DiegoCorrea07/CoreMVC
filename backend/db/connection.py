
from peewee import PostgresqlDatabase
from urllib.parse import urlparse
import os

DATABASE_URL = os.getenv("DATABASE_URL", "URL_DE BASE DE DATOS")

url = urlparse(DATABASE_URL)

db = PostgresqlDatabase(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
