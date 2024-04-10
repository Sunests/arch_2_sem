from fastapi import HTTPException, APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from article_workers.article import ArticleCRUD, ArticleExistsError, ArticleNotFoundError
from models.article import Article

router = APIRouter()

crud = ArticleCRUD()


@router.post("/articles", status_code=201)
async def create_article(article: Article):
    try:
        result = await crud.create(article)
    except ArticleExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return result


@router.get("/articles/{article_id}", status_code=200)
async def read_article(article_id: str):
    try:
        article = await crud.read(article_id)
    except ArticleNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return article


@router.put("/articles/{article_id}", status_code=200)
async def update_article(article_id: str, article: Article):
    try:
        await crud.update(article_id, article)
    except ArticleNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return article


@router.delete("/articles/{article_id}", status_code=204)
async def delete_article(article_id: str):
    try:
        await crud.delete(article_id)
    except ArticleNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/articles", status_code=200)
async def get_all_articles():
    return await crud.get_all()
