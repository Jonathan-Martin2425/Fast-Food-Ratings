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

# gets all the ingredients of a specific brand
@router.get("/{brand_id}/all_ingredients")
def get_brand_ingredients(brand_id: int):
    all_ing = []
    with db.engine.begin() as connection:
        ingredients = connection.execute(sqlalchemy.text("""SELECT ingredients.name FROM ingredients
                                                        JOIN food ON food.f_id = ingredients.food_id
                                                        JOIN brands on food.brand_id = brands.b_id
                                                        WHERE food.brand_id = :brand_id
                                                        ORDER BY name asc"""), {"brand_id": brand_id})
        brand = connection.execute(sqlalchemy.text("SELECT name FROM brands WHERE b_id = :brand_id"), {"brand_id": brand_id}).scalar()
    for i in ingredients:
        all_ing.append({
            "brand_id": brand_id,
            "brand_name": brand,
            "ingredient": i[0]
        })
    if len(all_ing) == 0:
        raise HTTPException(status_code=400, detail=f"There are no ingredients for that brand_id#{brand_id} or that brand_id does not exist")
    return all_ing


# gets all the ingredients of a specific food
@router.get("/{food_id}")
def get_food_ingredients(food_id: int):
    with db.engine.begin() as connection:
        ingredients = connection.execute(
            sqlalchemy.text("""
                SELECT ingredients.name FROM ingredients
                JOIN food ON food.f_id = ingredients.food_id
                WHERE food.f_id = :food_id
                ORDER BY name ASC
            """),
            {"food_id": food_id}
        ).fetchall()

        food = connection.execute(
            sqlalchemy.text("SELECT name FROM food WHERE f_id = :food_id"),
            {"food_id": food_id}
        ).scalar()

    if not food or not ingredients:
        raise HTTPException(
            status_code=400,
            detail=f"There are no ingredients for food_id #{food_id} or that food_id does not exist"
        )

    return {
        "food_id": food_id,
        "food": food,
        "ingredients": [i[0] for i in ingredients]
    }




    
        
        
        
        
            

    
    
    
    

