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


# given a brand id, returns all its locations
# if there are no locations or brand doesn't exist, raises 400 error with message
@router.get("/{brand_id}/")
def get_locations(brand_id: int):
    res = []
    with db.engine.begin() as connection:
        locations = connection.execute(
            sqlalchemy.text("SELECT name, l_id, address, b_id FROM brands "
                            "JOIN locations ON b_id = brand_id "
                            "WHERE brand_id = :brand"), {"brand": brand_id})
        for location in locations:
            res.append({
                "address": location.address,
                "address_id": location.l_id,
                "brand": location.name,
                "brand_id": location.b_id
            })

    if not res:
        # raises bad input error on incorrect location or brand id
        raise HTTPException(status_code=400, detail="There is no such brand")

    return res


@router.get("/{brand_id}/top_locations")
def get_top_locations(brand_id: int):
    res = []
    with db.engine.begin() as connection:

        t = connection.execute(sqlalchemy.text("SELECT l_id, address, "
                                               "AVG(cleanliness_rating) AS avg_cleanliness, "
                                               "AVG(quality_rating) AS avg_quality, "
                                               "AVG(service_rating) AS avg_service, "
                                               "COUNT(r_id) AS num_reviews "
                                               "FROM locations "
                                               "LEFT JOIN reviews ON location_id = l_id "
                                               "WHERE brand_id = :b_id "
                                               "GROUP BY l_id, address "
                                               "ORDER BY l_id ASC"), {"b_id": brand_id})
        locations = []
        i = 0
        bestScores = [{
            "value": 0,
            "index": 0
        }] * 4
        for location in t:
            locations.append(location)
            if location.num_reviews <= 3:
                i += 1
                continue
            totalScore = location.avg_cleanliness + location.avg_quality + location.avg_service
            if totalScore > bestScores[0]['value']:
                bestScores[0] = {
                    "value": totalScore,
                    "index": i
                }
            if location.avg_cleanliness >= bestScores[1]['value']:
                bestScores[1] = {
                    "value": location.avg_cleanliness,
                    "index": i
                }
            if location.avg_quality >= bestScores[2]['value']:
                bestScores[2] = {
                    "value": location.avg_quality,
                    "index": i
                }
            if location.avg_service >= bestScores[3]['value']:
                bestScores[3] = {
                    "value": location.avg_service,
                    "index": i
                }
            i += 1

        if not locations:
            return [{"message": "There are no locations for this brand"}]

    types = ["Best Overall", "Best Cleanliness", "Best Quality", "Best Service"]
    for i in range(4):

        # checks if any reviews were used in aggregation before adding all the best scores to the result
        if locations[bestScores[i]["index"]].avg_service is None:
            res.append({
                "message": "there are no reviews for any location from this brand"
            })
            break
        else:
            res.append({
                "type": types[i],
                "Overall Score": (locations[bestScores[i]["index"]].avg_cleanliness +
                                  locations[bestScores[i]["index"]].avg_quality +
                                  locations[bestScores[i]["index"]].avg_service) / 3,
                "Cleanliness": locations[bestScores[i]["index"]].avg_cleanliness,
                "Quality": locations[bestScores[i]["index"]].avg_quality,
                "Service": locations[bestScores[i]["index"]].avg_service,
                "address": locations[bestScores[i]["index"]].address,
                "location_id": locations[bestScores[i]["index"]].l_id,
                "brand_id": brand_id
            })

    return res