from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/brands",
    tags=["brands"],
    dependencies=[Depends(auth.get_api_key)],
)


class Review(BaseModel):
    publisher_id: int
    description: str
    service: int
    quality: int
    cleanliness: int


# given a brand id, returns all its locations
# if there are no locations or brand doesn't exist, raises 400 error with message
@router.get("/{brand_id}/")
def get_locations(brand_id: int):
    res = []
    with db.engine.begin() as connection:
        locations = connection.execute(
            sqlalchemy.text("SELECT name, address FROM brands "
                            "JOIN locations ON b_id = brand_id "
                            "WHERE brand_id = :brand"), {"brand": brand_id})
        for location in locations:
            res.append({
                "address": location.address,
                "brand": location.name
            })

    if len(res) <= 0:
        # raises bad input error on incorrect location or brand id
        raise HTTPException(status_code=400, detail="There is no such brand")

    return res


# Given a correct location with its brand id, returns them and all reviews from that location
# if the brand or location ids are incorrect, then it gives an error message
@router.get("/{brand_id}/location/{location_id}")
def get_reviews(brand_id: int, location_id: int):
    res = []
    with db.engine.begin() as connection:

        # gets brand name and address
        location_data = {
            "brand": brand_id,
            "location": location_id
        }
        try:
            brand, address = connection.execute(
                sqlalchemy.text("SELECT name, address FROM brands "
                                "JOIN locations ON b_id = brand_id "
                                "WHERE brand_id = :brand AND l_id = :location"), location_data).one()
        except sqlalchemy.exc.NoResultFound:

            # raises bad input error on incorrect location or brand id
            raise HTTPException(status_code=400, detail="There is no such location")

        # adds brand name and address to top of response
        res.append({
            "brand": brand,
            "address": address
        })

        # gets all reviews from the given location
        reviews = connection.execute(sqlalchemy.text(
            "SELECT date_published, name, service_rating, quality_rating, cleanliness_rating, description FROM reviews "
            "JOIN users ON publisher_id = u_id "
            "WHERE location_id = :location"), location_data)

        # iterates through reviews and adds each one to response
        for review in reviews:
            res.append({
                "publisher": review.name,
                "description": review.description,
                "ratings (S, Q, C)": [review.service_rating, review.quality_rating, review.cleanliness_rating],
                "date_published": review.date_published
            })
        if len(res) == 1:
            res.append({"message": "There are no reviews for this locations. Try making one!"})

    return res


# adds a review given all the known parameters
@router.post("/{brand_id}/location/{location_id}")
def submit_review(review: Review, brand_id: int, location_id: int):
    with db.engine.begin() as connection:
        # gets username from user's id
        username = connection.execute(sqlalchemy.text("SELECT name FROM users WHERE u_id = :id"),
                                      {"id": review.publisher_id}).one().name

        # gets brand name and address/location_name from ids
        brand_dict = {"location": location_id,
                      "brand": brand_id}
        try:
            brand_name, address = connection.execute(
                sqlalchemy.text("SELECT name, address FROM brands "
                                "JOIN locations ON b_id = brand_id "
                                "WHERE brand_id = :brand AND l_id = :location"), brand_dict).one()
        except sqlalchemy.exc.NoResultFound:

            # raises bad input error on incorrect location or brand id
            raise HTTPException(status_code=400, detail="There is no such location")

        # adds review to reviews table
        review_data = {
            "l_id": location_id,
            "p_id": review.publisher_id,
            "description": review.description,
            "s": review.service,
            "q": review.quality,
            "c": review.cleanliness,
            "location": address,
        }
        connection.execute(sqlalchemy.text("INSERT INTO reviews (location_id, publisher_id, description, "
                                           "service_rating, quality_rating, cleanliness_rating) "
                                           "VALUES (:l_id, :p_id, :description, :s, :q, :c)"), review_data)

        connection.execute(sqlalchemy.text("INSERT INTO visited (user_id, visit) "
                                           "VALUES (:p_id, :location)"), review_data)

        # returns review made to user
        res = [{
            "publisher": username,
            "brand": brand_name,
            "address": address,
            "description": review.description,
            "ratings (S, Q, C)": [review.service, review.quality, review.cleanliness]
        }]
    return res
