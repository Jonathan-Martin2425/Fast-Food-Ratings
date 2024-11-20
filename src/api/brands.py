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


class Username(BaseModel):
    username: str


# given a brand id, returns all its locations
# if there are no locations or brand doesn't exist, raises 400 error with message
@router.get("/{brand_id}/")
def get_locations(brand_id: int):
    res = []
    with db.engine.begin() as connection:
        locations = connection.execute(
            sqlalchemy.text("SELECT name, l_id, address FROM brands "
                            "JOIN locations ON b_id = brand_id "
                            "WHERE brand_id = :brand"), {"brand": brand_id})
        for location in locations:
            res.append({
                "address": location.address,
                "address_id": location.l_id,
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


@router.get("/{brand_id}/top_locations")
def get_top_locations(brand_id: int):
    res = []
    with db.engine.begin() as connection:
        t = connection.execute(sqlalchemy.text("SELECT location_id, address, "
                                               "AVG(cleanliness_rating) AS avg_cleanliness, "
                                               "AVG(quality_rating) AS avg_quality, "
                                               "AVG(service_rating) AS avg_service, "
                                               "COUNT(r_id) AS num_reviews "
                                               "FROM locations "
                                               "JOIN reviews ON location_id = l_id "
                                               "WHERE brand_id = :b_id "
                                               "GROUP BY location_id, address "
                                               "ORDER BY location_id ASC"), {"b_id": brand_id})
        locations = []
        i = 0
        bestScores = [{
            "value": 0,
            "index": 0
        }] * 4
        for location in t:
            locations.append(location)
            totalScore = location.avg_cleanliness + location.avg_quality + location.avg_service
            if location.num_reviews <= 3:
                i += 1
                continue
            if totalScore > bestScores[0]['value']:
                bestScores[0] = {
                    "value": totalScore,
                    "index": i
                }
            if location.avg_cleanliness > bestScores[1]['value']:
                bestScores[1] = {
                    "value": location.avg_cleanliness,
                    "index": i
                }
            if location.avg_quality > bestScores[2]['value']:
                bestScores[2] = {
                    "value": location.avg_quality,
                    "index": i
                }
            if location.avg_service > bestScores[3]['value']:
                bestScores[3] = {
                    "value": location.avg_service,
                    "index": i
                }
            i += 1

        if len(locations) == 0:
            raise HTTPException(status_code=500, detail="There are no reviews for any locations")

    types = ["Best Overall", "Best Cleanliness", "Best Quality", "Best Service"]
    for i in range(4):
        res.append({
            "type": types[i],
            "Overall Score": (locations[bestScores[i]["index"]].avg_cleanliness +
                              locations[bestScores[i]["index"]].avg_quality +
                              locations[bestScores[i]["index"]].avg_service) / 3,
            "Cleanliness": locations[bestScores[i]["index"]].avg_cleanliness,
            "Quality": locations[bestScores[i]["index"]].avg_quality,
            "Service": locations[bestScores[i]["index"]].avg_service,
            "address": locations[bestScores[i]["index"]].address,
            "location_id": locations[bestScores[i]["index"]].location_id
        })

    return res


@router.post("/signup")
def add_user(username: Username):
    actualUname = username.username.strip()
    if len(actualUname) >= 30:
        raise HTTPException(status_code=400, detail="name too long, max 30 characters")
    elif len(actualUname) <= 4:
        raise HTTPException(status_code=400, detail="name too small, min 4 characters")
    with db.engine.begin() as connection:
        t = connection.execute(sqlalchemy.text("SELECT name FROM users"))
        for name in t:
            if name.name == actualUname:
                raise HTTPException(status_code=400, detail="Username already exists")
        connection.execute(sqlalchemy.text("INSERT INTO users (name) VALUES"
                                           "(:name)"), {"name": actualUname})
        return []
