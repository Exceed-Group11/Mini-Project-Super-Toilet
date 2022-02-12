from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
mongo_client = MongoClient('mongodb://localhost', 27017)

db = mongo_client["SuperToilet"]
collection = db["Toilets"]


@app.get("/toilet/{toilet_id}")
def show_status(toilet_id: int):
    check = collection.find({"toilet_id": toilet_id}, {
                            "_id": 0, "toilet_id": 0})
    list_check = list(check)
    # TODO: Check if the toilet_id is found.
    return list_check.pop()
