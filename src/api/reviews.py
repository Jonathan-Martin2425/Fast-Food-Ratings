from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
    dependencies=[Depends(auth.get_api_key)],
)


class Review(BaseModel):
    publisher_id: int
    description: str
    service: int
    quality: int
    cleanliness: int


class ReviewUpdate(BaseModel):
    description: str
    service: int
    quality: int
    cleanliness: int


# Given a correct location with its brand id, returns them and all reviews from that location
# if the brand or location ids are incorrect, then it gives an error message
@router.get("/{brand_id}/location/{location_id}")
def get_reviews(brand_id: int, location_id: int):
    res = []
    with db.engine.begin() as connection:

        # gets brand name and address, also checking if they exist
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
            raise HTTPException(status_code=400, detail="There is no such location or brand")

        # adds brand name and address to top of response
        res.append({
            "brand": brand,
            "brand_id": brand_id,
            "address": address,
            "address_id": location_id,
        })

        # gets all reviews from the given location
        reviews = connection.execute(sqlalchemy.text(
            "SELECT DATE(date_published) as date, name, publisher_id, "
            "service_rating, quality_rating, cleanliness_rating, description, r_id FROM reviews "
            "JOIN users ON publisher_id = u_id "
            "WHERE location_id = :location "
            "ORDER BY date_published ASC"), location_data)

        # iterates through reviews and adds each one to response
        for review in reviews:
            res.append({
                "description": review.description,
                "ratings (S, Q, C)": [review.service_rating, review.quality_rating, review.cleanliness_rating],
                "date_published": review.date,
                "publisher": review.name,
                "publisher_id": review.publisher_id,
                "review_id": review.r_id
            })
        if len(res) == 1:
            res.append({"message": "There are no reviews for this locations. Try making one!"})

    return res


# adds a review given all the known parameters
@router.post("/{brand_id}/location/{location_id}", status_code=201)
def submit_review(review: Review, brand_id: int, location_id: int):
    with db.engine.begin() as connection:

        # checks if review attributes are valid
        if review.publisher_id is None or review.publisher_id <= 0:
            raise HTTPException(status_code=400, detail="Invalid publisher id")
        if review.service is None or review.service < 0 or review.service > 10 or \
                review.quality is None or review.quality < 0 or review.quality > 10 or \
                review.cleanliness is None or review.cleanliness < 0 or review.cleanliness > 10:
            raise HTTPException(status_code=400, detail="Invalid ratings. Service, Quality and Cleanliness "
                                                        "must be integers between or equal to 0-10")

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
            "service_rating": review.service,
            "quality_rating": review.quality,
            "cleanliness_rating": review.cleanliness,
            "location": address,
        }
        r_id = connection.execute(sqlalchemy.text("INSERT INTO reviews (location_id, publisher_id, description, "
                                                  "service_rating, quality_rating, cleanliness_rating) "
                                                  "VALUES (:l_id, :p_id, :description, :service_rating, "
                                                  ":quality_rating, :cleanliness_rating) "
                                                  "RETURNING r_id"), review_data).one().r_id

        connection.execute(sqlalchemy.text("INSERT INTO visited (user_id, visit) "
                                           "VALUES (:p_id, :location)"), review_data)

        # returns review made to user
        res = [{
            "publisher": username,
            "brand": brand_name,
            "address": address,
            "description": review.description,
            "ratings (Service, Quality, Cleanliness)": [review.service, review.quality, review.cleanliness],
            "r_id": r_id
        }]
    return res


@router.delete("{username}/review/{r_id}")
def delete_review(username: str, r_id: int):
    with db.engine.begin() as connection:

        # checks if review or user exists and gives 400 error if it doesn't
        review_dict = {
            "r_id": r_id,
            "name": username
        }
        review = connection.execute(sqlalchemy.text("SELECT u_id FROM users "
                                                    "JOIN reviews ON publisher_id = u_id "
                                                    "WHERE r_id= :r_id AND name = :name"), review_dict)
        i = 0
        for r in review:
            review_dict["u_id"] = r.u_id
            i += 1
        if i < 1:
            raise HTTPException(status_code=400, detail="review or user does not exist.")

        # deletes review given the user and review ids
        connection.execute(sqlalchemy.text("DELETE FROM reviews "
                                           "WHERE r_id = :r_id AND publisher_id = :u_id"), review_dict)
    return []


@router.patch("{username}/review/{r_id}")
def update_review(username: str, r_id: int, newReview: ReviewUpdate):
    # checks if newReview has valid inputs
    if newReview.description is None or newReview.service > 10 or newReview.service < 0 or \
            newReview.quality > 10 or newReview.quality < 0 or newReview.cleanliness > 10 or newReview.cleanliness < 0:
        raise HTTPException(status_code=400, detail="invalid review changes")

    with db.engine.begin() as connection:

        # checks if review or user exists and gives 400 error if it doesn't
        review_ids = {
            "r_id": r_id,
            "name": username
        }
        review = connection.execute(sqlalchemy.text("SELECT u_id, address FROM users "
                                                    "JOIN reviews ON publisher_id = u_id "
                                                    "LEFT JOIN locations ON location_id = l_id "
                                                    "WHERE r_id= :r_id AND name = :name"), review_ids)
        i = 0
        for r in review:
            review_ids["u_id"] = r.u_id
            review_ids["location"] = r.address
            i += 1
        if i < 1:
            raise HTTPException(status_code=400, detail="review or user does not exist.")

        # updates the review given user and review ids
        review_dict = {
            "description": newReview.description,
            "s_rating": newReview.service,
            "q_rating": newReview.quality,
            "c_rating": newReview.cleanliness,
            "u_id": review_ids["u_id"],
            "r_id": r_id
        }
        connection.execute(sqlalchemy.text("UPDATE reviews "
                                           "SET description = :description, service_rating = :s_rating, "
                                           "quality_rating = :q_rating, cleanliness_rating = :c_rating "
                                           "WHERE publisher_id = :u_id AND r_id = :r_id"), review_dict)
        connection.execute(sqlalchemy.text("INSERT INTO visited (user_id, visit) "
                                           "VALUES (:u_id, :location)"), review_ids)
    return review_dict
