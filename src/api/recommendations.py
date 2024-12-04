from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
    dependencies=[Depends(auth.get_api_key)],
)

# @router.get("/{username}")
# def recommend_restuarants(username: str):
    



