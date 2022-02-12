from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
mongo_client = MongoClient('mongodb://localhost', 27017)

db = mongo_client["SuperToilet"]
