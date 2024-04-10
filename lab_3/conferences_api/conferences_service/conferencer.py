from bson import ObjectId
from fastapi import HTTPException
from connector.mongo_connector import MongoConnector
from models.conferences import ConferenceModel


class ConferenceService:
    async def create_conference(self, conference_data: dict):
        collection = await MongoConnector.get_collection()
        new_conference = conference_data.copy()
        new_conference["_id"] = str(
            (await collection.insert_one(new_conference)).inserted_id)
        return new_conference

    async def get_all_conferences(self):
        collection = await MongoConnector.get_collection()
        conferences = []
        async for doc in collection.find():
            doc["_id"] = str(doc["_id"])
            conferences.append(doc)
        return conferences

    async def get_conference(self, conference_id: str):
        collection = await MongoConnector.get_collection()
        conference = await collection.find_one({"_id": ObjectId(conference_id)})
        if not conference:
            raise HTTPException(status_code=404, detail="Conference not found")
        return ConferenceModel(**conference)

    async def update_conference(self, conference_id: str, conference_data: dict):
        collection = await MongoConnector.get_collection()
        conference_update = conference_data.copy()
        conference_update.pop("_id", None)
        result = await collection.update_one(
            {"_id": ObjectId(conference_id)}, {"$set": conference_update})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Conference not found")
        return conference_update

    async def delete_conference(self, conference_id: str):
        collection = await MongoConnector.get_collection()
        result = await collection.delete_one({"_id": ObjectId(conference_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Conference not found")
        return {"message": "Conference deleted"}
