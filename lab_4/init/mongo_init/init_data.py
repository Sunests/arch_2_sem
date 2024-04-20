from typing import List
from faker import Faker
from pymongo import MongoClient
from pymongo.collection import Collection
import json
import random


class DataIniter:

    @staticmethod
    def get_fake_conference(articles_collection: Collection, conferences_collection: Collection, users_ids: List[int]):
        fake = Faker()
        count_of_confs = fake.random_int(min=11, max=11)
        confs = []
        with open("./mongo_init/conferences.json", "r") as json_file:
            data = json.load(json_file)
            for conference in data:
                for article in conference["articles"]:
                    article["author_id"] = random.choice(users_ids)
                articles_ids = articles_collection.insert_many(
                    conference["articles"]).inserted_ids
                conference["articles"] = articles_ids
                confs.append(
                    {
                        "name": conference["name"],
                        "articles": articles_ids,
                        "dates_of_conference": conference["name"],
                    }
                )
        conferences_collection.insert_many(confs)


class MongoConnector:
    _instance = None

    def get_collection(self, collection_name: str):
        if self._instance is None:
            username = "root"
            password = "example"
            mongo_uri = f"mongodb://{username}:{password}@mongo:27017/"
            self._instance = MongoClient(mongo_uri)
        database = self._instance["arch"]
        collection = database[collection_name]
        return collection

    def init(self, users_ids: List[int]):
        print("Start mongo initializtion")
        conferences_collection = self.get_collection(
            collection_name="conferences")
        articles_collection = self.get_collection(
            collection_name="articles")
        articles_collection.drop()
        conferences_collection.drop()
        DataIniter.get_fake_conference(
            articles_collection, conferences_collection, users_ids)
        print(conferences_collection.find_one())
        print(articles_collection.find_one())
        print("Mongo successfully inited")
