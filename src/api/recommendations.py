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

class UserRecommendation(BaseModel):
    username: str

# Recommends restaurants to a user based on their review history.
@router.get("/{username}")
def recommend_restaurants(username: str):
    with db.engine.begin() as connection:
        user_reviews = connection.execute(
            sqlalchemy.text("""
                SELECT r_id, COUNT(*) as review_count
                FROM reviews
                JOIN locations ON locations.l_id = reviews.location_id
                WHERE publisher_id = (SELECT u_id FROM users WHERE name = :username)
                GROUP BY r_id
                ORDER BY review_count DESC
                LIMIT 1
            """),
            {"username": username}
        ).fetchone()

        if not user_reviews:
            raise HTTPException(status_code=404, detail=f"No reviews found for user '{username}'.")

        most_reviewed_brand = user_reviews.r_id

        recommendations = connection.execute(
            sqlalchemy.text("""
                SELECT DISTINCT locations.l_id, locations.address, brands.name as brand_name
                FROM locations
                JOIN brands ON brands.b_id = locations.brand_id
                WHERE locations.brand_id = :brand_id
                  AND locations.l_id NOT IN (
                      SELECT location_id FROM reviews
                      WHERE publisher_id = (SELECT u_id FROM users WHERE name = :username)
                  )
                ORDER BY locations.l_id ASC
                LIMIT 5
            """),
            {"brand_id": most_reviewed_brand, "username": username}
        ).fetchall()

        if not recommendations:
            return {"message": "No new recommendations available for this user."}

        result = [
            {
                "location_id": rec.l_id,
                "address": rec.address,
                "brand_name": rec.brand_name
            }
            for rec in recommendations
        ]
    return result
    



