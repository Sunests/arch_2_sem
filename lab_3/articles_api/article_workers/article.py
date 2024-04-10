from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from typing import List
from connector.mongo_connector import MongoConnector
from models.article import Article


class ArticleCRUD:

    async def create(self, article: Article) -> Article:
        try:
            collection = await MongoConnector.get_collection()
            mongo_response = await collection.insert_one(article.model_dump())
            result = {"_id": str(mongo_response.inserted_id)}
        except DuplicateKeyError:
            raise ArticleExistsError(f"Article with title '{
                                     article.title}' already exists")
        return result

    async def read(self, article_id: str) -> Article:
        collection = await MongoConnector.get_collection()
        article = await collection.find_one({"_id": ObjectId(article_id)})
        if not article:
            raise ArticleNotFoundError(
                f"Article with ID '{article_id}' not found")
        return Article(**article)

    async def update(self, article_id: str, article: Article) -> Article:
        collection = await MongoConnector.get_collection()
        updated_article = await collection.update_one(
            {"_id": ObjectId(article_id)}, {"$set": article.model_dump()}
        )
        if updated_article.modified_count == 0:
            raise ArticleNotFoundError(
                f"Article with ID '{article_id}' not found")
        return article

    async def delete(self, article_id: str):
        collection = await MongoConnector.get_collection()
        deleted_article = await collection.delete_one({"_id": ObjectId(article_id)})
        if deleted_article.deleted_count == 0:
            raise ArticleNotFoundError(
                f"Article with ID '{article_id}' not found")

    async def get_all(self) -> List[Article]:
        articles = []
        collection = await MongoConnector.get_collection()
        async for cursor in collection.find():
            articles.append(Article(**cursor))
        return articles


class ArticleNotFoundError(Exception):
    pass


class ArticleExistsError(Exception):
    pass
