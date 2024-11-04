from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/endpoints",
    tags=["endpoints"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/{brand_id}")
async def root():
    return {"message": "Welcome to Fast-Food-Ratings, for all your fast food needs."}
