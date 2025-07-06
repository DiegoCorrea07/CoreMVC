
import os

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SECRET_KEY = os.getenv("SECRET_KEY", "AdminCoreSecretKey")