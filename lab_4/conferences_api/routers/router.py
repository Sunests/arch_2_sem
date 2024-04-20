from fastapi import APIRouter, HTTPException, Body
from models.conferences import ConferenceModel, ConferenceUpdateModel
from conferences_service.conferencer import ConferenceService
from bson.errors import InvalidId

router = APIRouter()
conference_service = ConferenceService()


@router.get("/get_all_conferences")
async def get_all_conferences():
    try:
        result = await conference_service.get_all_conferences()
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise e
    return result


@router.get("/conferences")
async def get_conference(conference_id: str):
    try:
        result = await conference_service.get_conference(conference_id)
    except InvalidId:
        raise HTTPException(
            status_code=400, detail=f'Invalid ID of conference "{conference_id}"')
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise e
    return result


@router.post("/conferences")
async def create_conference(conference_data: ConferenceModel):
    try:
        result = await conference_service.create_conference(conference_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise e
    return {"message": f"Succesfully created with id {result}"}


@router.put("/conferences")
async def update_conference(conference_id: str, conference_data: ConferenceUpdateModel):
    try:
        result = await conference_service.update_conference(conference_id, conference_data)
    except InvalidId:
        raise HTTPException(
            status_code=400, detail=f'Invalid ID of conference "{conference_id}"')
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise e
    return result


@router.delete("/conferences")
async def delete_conference(conference_id: str):
    try:
        result = await conference_service.delete_conference(conference_id)
    except InvalidId:
        raise HTTPException(
            status_code=400, detail=f'Invalid ID of conference "{conference_id}"')
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise e
    return result
