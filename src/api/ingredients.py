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
    
# gets all of the ingredients in the ingredients database
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

# gets all the ingredients that a specific brand uses in all of their foods
@router.get("/{brand_id}/all_ingredients")
def get_brand_ingredients(brand_id: int):
    all = []
    with db.engine.begin() as connection:
        ingredients = connection.execute(sqlalchemy.text("""SELECT ingredients.name FROM ingredients
                                                        JOIN food ON food.f_id = ingredients.food_id
                                                        JOIN brands on food.brand_id = brands.b_id
                                                        WHERE food.brand_id = :brand_id
                                                        ORDER BY name asc"""), {"brand_id": brand_id})
        brand = connection.execute(sqlalchemy.text("SELECT name FROM brands WHERE b_id = :brand_id"), {"brand_id": brand_id}).scalar()
        for i in ingredients:
            print(i)
        
        
        
        
            

    
    
    
    

