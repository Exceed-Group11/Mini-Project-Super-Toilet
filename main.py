from utils.database.supertoilet_database import SuperToiletDatabase
from utils.calculate_average import calculate_average
from models.status_models import StatusModel
import datetime
from typing import Dict, final
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
supertoilet_database = SuperToiletDatabase()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient('mongodb://localhost', 27017)
db = client["SuperToilet"]

collection = db["Toilets"]


@app.get("/toilet/statistic/")
def get_toilet_statistic():
    try:
        toilet_stat = supertoilet_database.get_stat()
    except ValueError as e:
        raise HTTPException(500, {
            "message": str(e)
        })
    return {
        "time_average": toilet_stat["time_average"]
    }


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
    current_time_stamp = int(datetime.datetime.now().timestamp())
    if status_obj.status:
        update_toilet_object = {
            "status": status_obj.status,
            "time_in": current_time_stamp
        }
    else:
        # Get current time_in and calculate time diff
        time_in = focused_toilet["time_in"]
        time_diff = current_time_stamp - time_in
        # Get current statistic data
        stat = supertoilet_database.get_stat()
        # Calculate new average
        new_stat, count = calculate_average(
            stat["time_average"], stat["count"], time_diff)
        # Set new average data
        supertoilet_database.set_stat({
            "time_average": new_stat,
            "count": count
        })
        update_toilet_object = {
            "status": status_obj.status,
            "time_in": None
        }
    toilet_collection.update_one({"toilet_id": toilet_id}, {
        "$set": update_toilet_object})
    return {
        "message": "success"
    }


@app.get("/toilet/")
def show_all():
    find_all = collection.find({}, {"_id": 0})
    list_find = []
    for find in find_all:
        list_find.append(find)
    return {
        "result": list_find
    }
