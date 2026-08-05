from pymongo.asynchronous.collection import AsyncCollection

from app.db.db import database

COLLECTION_NAME = "files"

files_collection: AsyncCollection = database[COLLECTION_NAME]