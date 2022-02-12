from typing import Dict
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import datetime

from models.status_models import StatusModel

app = FastAPI()
mongo_client = MongoClient('mongodb://localhost', 27017)

db = mongo_client["SuperToilet"]

collection = db["Toilets"]


@app.get("/toilet/{toilet_id}/")
def show_status(toilet_id: int):
    check = collection.find({"toilet_id": toilet_id}, {
                            "_id": 0, "toilet_id": 0})
    list_check = list(check)
    if len(list_check) == 0:
        raise HTTPException(404, f"Couldn't find toilet_id:{toilet_id}")
    return list_check.pop()


@app.post("/toilet/{toilet_id}/")
def update_toilet_status(toilet_id: int, status_obj: StatusModel):
    # Check if the toilet is valid
    toilet_collection = db["Toilets"]
    query_toilet = toilet_collection.find({"toilet_id": toilet_id}, {"_id": 0})
    list_query_toilet = list(query_toilet)

    if len(list_query_toilet) != 1:
        raise HTTPException(400, {
            "message": "The toilet id was not found or the data is broken."
        })

    focused_toilet = list_query_toilet.pop()
    if focused_toilet["status"] == status_obj.status:
        raise HTTPException(400, {
            "message": f"The toilet is already in status {status_obj.status}"
        })

    update_toilet_object = {}
    if status_obj.status:
        update_toilet_object = {
            "status": status_obj.status,
            "time_in": int(datetime.datetime.now().timestamp())
        }
    else:
        update_toilet_object = {
            "status": status_obj.status,
            "time_in": None
        }
    toilet_collection.update_one({"toilet_id": toilet_id}, {
        "$set": update_toilet_object})
    return {
        "message": "success"
    }


@app.get("/toilet/statistic/")
def get_toilet_statistic():
    toilet_stat_collection = db["ToiletStat"]
    list_toilet_stat = list(toilet_stat_collection.find({}))
    if len(list_toilet_stat) != 1:
        raise HTTPException(500, {
            "message": "The Statistic data is broken."
        })

    toilet_stat: Dict = list_toilet_stat.pop()
    # TODO: Maybe, Improve this later?
    if toilet_stat.get("time_average", "") == "":
        raise HTTPException(500, {
            "message": "The Statistic data is broken."
        })
    return {
        "toilet_average":  toilet_stat.get("time_average")
    }
