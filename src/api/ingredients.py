from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
from src.api import brands
import sqlalchemy
from src import database as db


router = APIRouter(
    prefix="/ingredients",
    tags=["ingredients"],
    dependencies=[Depends(auth.get_api_key)],
)

class Ingredient(BaseModel):
    food_id: int
    name: str
    
@router.get("/")
def get_ingredients():
    all = []
    with db.engine.begin() as connection:
        ingredients = connection.execute(sqlalchemy.text("SELECT ingredient_id, name FROM ingredients"))
    
    for ingredient in ingredients:
        all.append({
            "id": ingredient.ingredient_id,
            "name": ingredient.name
        })
    return all

    
    
    
    

