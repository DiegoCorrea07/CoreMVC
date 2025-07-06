from peewee import PostgresqlDatabase
from urllib.parse import urlparse
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://core_db_bcx4_user:IsHIQ3x7IOe3xL88Z9txFzXrYdFyJijg@dpg-d1f0dl6r433s73fnnth0-a.oregon-postgres.render.com/core_db_bcx4")

url = urlparse(DATABASE_URL)

db = PostgresqlDatabase(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
