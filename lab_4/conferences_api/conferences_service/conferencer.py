from bson import ObjectId
from fastapi import HTTPException
from connector.mongo_connector import MongoConnector
from models.conferences import ConferenceModel, ConferenceUpdateModel
import requests


class ConferenceService:

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

    async def create_conference(self, conference_data: ConferenceModel):
        collection = await MongoConnector.get_collection()
        conference = conference_data.model_dump()
        for article_id in conference_data.articles:
            try:
                if requests.get(
                        f"http://articles:8080/api/articles?article_id={article_id}").status_code != 200:
                    raise HTTPException(
                        status_code=400, detail=f'Invalid article id "{article_id}"')
            except HTTPException as e:
                raise e
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=503, detail=f"Сервис проверки статей недоступен!")
        conference_id = str(
            (await collection.insert_one(conference)).inserted_id)
        return conference_id

    async def update_conference(self, conference_id: str, conference_data: ConferenceUpdateModel):
        collection = await MongoConnector.get_collection()
        conference_update = {
            k: v for k, v in conference_data.model_dump().items() if v is not None}
        if conference_data.articles:
            for article_id in conference_data.articles:
                try:
                    if requests.get(
                            f"http://articles:8080/api/articles?article_id={article_id}").status_code != 200:
                        raise HTTPException(
                            status_code=400, detail=f'Invalid article id "{article_id}"')
                except HTTPException as e:
                    raise e
                except Exception as e:
                    print(e)
                    raise HTTPException(
                        status_code=503, detail=f"Сервис проверки статей недоступен!")
        result = await collection.update_one(
            {"_id": ObjectId(conference_id)}, {"$set": conference_update})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Conference not found")
        return conference_update

    async def delete_conference(self, conference_id: str):
        collection = await MongoConnector.get_collection()
        result = await collection.delete_one({"_id": ObjectId(conference_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Conference not found")
        return {"message": "Conference deleted"}
