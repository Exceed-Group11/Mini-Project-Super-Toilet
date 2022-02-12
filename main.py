from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
mongo_client = MongoClient('mongodb://localhost', 27017)

db = mongo_client["SuperToilet"]

collection = db["Toilets"]


class Toilet(Basemodel):
    toilet_id: int
    status: bool
    time_in: int


@app.get("/toilet/{toilet_id}/")
def show_status(toilet_id: int):
    check = collection.find({"toilet_id": toilet_id}, {"_id": 0})
    list_check = list(check)
    if len(list_check) == 0:
        raise HTTPException(404, f"Couldn't find toilet_id:{toilet_id}")
    return list_check.pop()
