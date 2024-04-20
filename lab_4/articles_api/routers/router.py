from fastapi import HTTPException, APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from article_workers.article import ArticleCRUD
from models.article import Article
from bson.errors import InvalidId

router = APIRouter()

crud = ArticleCRUD()


@router.get("/get_all_articles")
async def get_all_articles():
    return await crud.get_all()


@router.get(f"/articles")
async def read_article(article_id: str):
    try:
        article = await crud.read(article_id)
    except InvalidId as e:
        raise HTTPException(status_code=400, detail="Invalid id")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise e
    return article


@router.post("/articles")
async def create_article(article: Article):
    try:
        result = await crud.create(article)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise e
    return result


@router.put("/articles")
async def update_article(article_id: str, article: Article):
    try:
        result = await crud.update(article_id, article)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise e
    return {"message": f"Article with id {article_id} was successfully updated"}


@router.delete("/articles")
async def delete_article(article_id: str):
    try:
        await crud.delete(article_id)
    except HTTPException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise e
    return {"message": f"Article with id {article_id} was successfully updated"}
