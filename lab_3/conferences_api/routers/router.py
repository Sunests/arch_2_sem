from fastapi import APIRouter, HTTPException, Body
from models.conferences import ConferenceModel
from conferences_service.conferencer import ConferenceService

router = APIRouter()
conference_service = ConferenceService()


@router.post("/conferences/", response_model=dict, status_code=201)
async def create_conference(conference_data: dict = Body(...)):
    return await conference_service.create_conference(conference_data)


@router.get("/conferences/", response_model=list[dict])
async def get_all_conferences():
    return await conference_service.get_all_conferences()


@router.get("/conferences/{conference_id}", response_model=ConferenceModel)
async def get_conference(conference_id: str):
    return await conference_service.get_conference(conference_id)


@router.put("/conferences/{conference_id}", response_model=ConferenceModel)
async def update_conference(conference_id: str, conference_data: dict = Body(...)):
    return await conference_service.update_conference(conference_id, conference_data)


@router.delete("/conferences/{conference_id}", response_model=dict)
async def delete_conference(conference_id: str):
    return await conference_service.delete_conference(conference_id)
