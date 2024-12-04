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
@router.get("/{brand_id}/all_ingredients")
def get_brand_ingredients(brand_id: int):
    with db.engine.begin() as connection:
        ingredients = connection.execute(
            sqlalchemy.text("""
                SELECT DISTINCT ingredients.name FROM ingredients
                JOIN food ON food.f_id = ingredients.food_id
                JOIN brands ON food.brand_id = brands.b_id
                WHERE food.brand_id = :brand_id
                ORDER BY ingredients.name ASC
            """),
            {"brand_id": brand_id}
        ).fetchall()

        brand = connection.execute(
            sqlalchemy.text("SELECT name FROM brands WHERE b_id = :brand_id"),
            {"brand_id": brand_id}
        ).scalar()

    if not brand or not ingredients:
        raise HTTPException(
            status_code=400,
            detail=f"There are no ingredients for brand_id #{brand_id} or that brand_id does not exist"
        )
    return {
        "brand_id": brand_id,
        "brand_name": brand,
        "ingredients": [i[0] for i in ingredients]
    }



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
    
# Analyze the impact of an ingredient on the average ratings of brands.
@router.get("/{ingredient_id}/impact_on_reviews")
def get_ingredient_impact_on_reviews(ingredient_id: int):
    try:
        with db.engine.begin() as connection:
            # Step 1: Fetch all brands and locations using the ingredient
            ingredient_locations = connection.execute(
                sqlalchemy.text("""
                    SELECT DISTINCT locations.l_id, brands.name AS brand_name, locations.address
                    FROM ingredients
                    JOIN food ON food.f_id = ingredients.food_id
                    JOIN locations ON locations.brand_id = food.brand_id
                    JOIN brands ON brands.b_id = locations.brand_id
                    WHERE ingredients.ingredient_id = :ingredient_id
                """),
                {"ingredient_id": ingredient_id}
            ).fetchall()

            if not ingredient_locations:
                raise HTTPException(
                    status_code=404, 
                    detail=f"No locations found using ingredient with ID {ingredient_id}."
                )

            # Step 2: Calculate average ratings for locations with the ingredient
            with_ratings = connection.execute(
                sqlalchemy.text("""
                    SELECT AVG(service_rating) AS avg_service, 
                           AVG(quality_rating) AS avg_quality, 
                           AVG(cleanliness_rating) AS avg_cleanliness
                    FROM reviews
                    WHERE location_id IN (
                        SELECT locations.l_id
                        FROM ingredients
                        JOIN food ON food.f_id = ingredients.food_id
                        JOIN locations ON locations.brand_id = food.brand_id
                        WHERE ingredients.ingredient_id = :ingredient_id
                    )
                """),
                {"ingredient_id": ingredient_id}
            ).fetchone()

            # Step 3: Calculate average ratings for locations without the ingredient
            without_ratings = connection.execute(
                sqlalchemy.text("""
                    SELECT AVG(service_rating) AS avg_service, 
                           AVG(quality_rating) AS avg_quality, 
                           AVG(cleanliness_rating) AS avg_cleanliness
                    FROM reviews
                    WHERE location_id NOT IN (
                        SELECT locations.l_id
                        FROM ingredients
                        JOIN food ON food.f_id = ingredients.food_id
                        JOIN locations ON locations.brand_id = food.brand_id
                        WHERE ingredients.ingredient_id = :ingredient_id
                    )
                """),
                {"ingredient_id": ingredient_id}
            ).fetchone()

            # Step 4: Handle edge cases for no reviews
            if not with_ratings and not without_ratings:
                raise HTTPException(
                    status_code=404, 
                    detail=f"No reviews found for analysis with or without ingredient ID {ingredient_id}."
                )

            # Step 5: Format the response
            response = {
                "ingredient_id": ingredient_id,
                "locations_with_ingredient": [
                    {"location_id": loc.l_id, "brand_name": loc.brand_name, "address": loc.address}
                    for loc in ingredient_locations
                ],
                "ratings_with_ingredient": {
                    "service": with_ratings.avg_service or 0,
                    "quality": with_ratings.avg_quality or 0,
                    "cleanliness": with_ratings.avg_cleanliness or 0,
                },
                "ratings_without_ingredient": {
                    "service": without_ratings.avg_service or 0,
                    "quality": without_ratings.avg_quality or 0,
                    "cleanliness": without_ratings.avg_cleanliness or 0,
                },
            }

        return response

    except sqlalchemy.exc.SQLAlchemyError as e:
        # Catch any database-related errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected database error occurred: {str(e)}"
        )
    except Exception as e:
        # Catch any other unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )





    
        
        
        
        
            

    
    
    
    

