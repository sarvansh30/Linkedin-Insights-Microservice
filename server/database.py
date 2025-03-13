from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

Mongo_URL=os.getenv("MONGO_URL")
DB_name=os.getenv("DB_NAME")

client =MongoClient(Mongo_URL)
db=client[DB_name]
pages_collection=db["pages"]
