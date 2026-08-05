import os

from dotenv import load_dotenv

from .client import mongo_client

load_dotenv()

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "full_rag",
)

database = mongo_client[DATABASE_NAME]