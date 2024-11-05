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


class Review(BaseModel):
    publisher_id: int
    description: str
    service: int
    quality: int
    cleanliness: int


# adds a review given all the known parameters
@router.post("/{brand_id}/location/{location_id}")
def add_review(review: Review, brand_id: int, location_id: int):
    with db.engine.begin() as connection:
        # gets username from user's id
        username = connection.execute(sqlalchemy.text("SELECT name FROM users WHERE u_id = :id"),
                                      {"id": review.publisher_id}).one().name

        # gets brand name and address/location_name from ids
        brand_dict = {"location": location_id,
                      "brand": brand_id}
        brand_name, address = connection.execute(
            sqlalchemy.text("SELECT name, address FROM brands "
                            "JOIN locations ON b_id = brand_id "
                            "WHERE l_id = :location AND b_id = :brand"), brand_dict).one()

        # adds review to reviews table
        review_data = {
            "l_id": location_id,
            "p_id": review.publisher_id,
            "description": review.description,
            "s": review.service,
            "q": review.quality,
            "c": review.cleanliness
        }
        connection.execute(sqlalchemy.text("INSERT INTO reviews (location_id, publisher_id, description, "
                                           "service_rating, quality_rating, cleanliness_rating) "
                                           "VALUES (:l_id, :p_id, :description, :s, :q, :c)"), review_data)

        # returns review made to user
        res = [{
            "publisher": username,
            "brand": brand_name,
            "address": address,
            "description": review.description,
            "ratings (S, Q, C)": [review.service, review.quality, review.cleanliness]
        }]
    return res
