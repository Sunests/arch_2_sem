from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import List
from connector.mongo_connector import MongoConnector
from fastapi.exceptions import HTTPException
from models.article import Article


class ArticleCRUD:

    async def get_all(self):
        articles = []
        collection = await MongoConnector.get_collection()
        async for cursor in collection.find():
            cursor["_id"] = str(cursor["_id"])
            articles.append(cursor)
        return articles

    async def read(self, article_id: str):
        collection: AsyncIOMotorCollection = await MongoConnector.get_collection()
        article = await collection.find_one({"_id": ObjectId(article_id)})
        if article:
            article["_id"] = str(article["_id"])
        else:
            raise HTTPException(status_code=404,
                                detail=f"Article with ID '{
                                    article_id}' not found"
                                )
        return article

    async def create(self, article: Article) -> Article:
        try:
            collection: AsyncIOMotorCollection = await MongoConnector.get_collection()
            mongo_response = await collection.insert_one(article.model_dump())
            result = {"_id": str(mongo_response.inserted_id)}
        except DuplicateKeyError:
            raise HTTPException(status_code=400,
                                detail=f"Article with title '{
                                    article.title}' already exists"
                                )
        return result

    async def update(self, article_id: str, article: Article) -> Article:
        collection: AsyncIOMotorCollection = await MongoConnector.get_collection()
        updated_article = await collection.update_one(
            {"_id": ObjectId(article_id)}, {"$set": article.model_dump()}
        )

    async def delete(self, article_id: str):
        collection: AsyncIOMotorCollection = await MongoConnector.get_collection()
        deleted_article = await collection.delete_one({"_id": ObjectId(article_id)})
        if deleted_article.deleted_count == 0:
            raise HTTPException(status_code=404,
                                detail=f"Article with ID '{
                                    article_id}' not found"
                                )
