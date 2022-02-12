from typing import Dict
from pymongo import MongoClient


class SuperToiletDatabase:

    def __init__(self, database_name: str = "SuperToilet"):
        self.__mongo_client = MongoClient('mongodb://localhost', 27017)
        self.__current_db = self.__mongo_client[database_name]

    def get_stat(self) -> dict:
        toilet_stat_collection = self.__current_db["ToiletStat"]
        list_toilet_stat = list(toilet_stat_collection.find({}))
        if len(list_toilet_stat) != 1:
            raise ValueError("Not found the data")

        toilet_stat: Dict = list_toilet_stat.pop()
        if toilet_stat.get("time_average", "") == "" or toilet_stat.get("count", "") == "":
            raise ValueError("The time_average is broken")
        return toilet_stat

    def set_stat(self, stat_obj: Dict) -> None:
        current_stat = self.get_stat()
        toilet_stat_collection = self.__current_db["ToiletStat"]
        toilet_stat_collection.update_one(
            {"time_average": current_stat["time_average"]}, {"$set": stat_obj})
        return None
