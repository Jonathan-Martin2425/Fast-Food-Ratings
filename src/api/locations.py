from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/locations",
    tags=["locations"],
    dependencies=[Depends(auth.get_api_key)],
)


# given a brand id, returns all its locations
# if there are no locations or brand doesn't exist, raises 400 error with message
@router.get("/{location_id}")
def get_location_hours(location_id: int):
    res = []
    with db.engine.begin() as connection:
        locations = connection.execute(
            sqlalchemy.text("SELECT name, l_id, address, b_id, day_name, "
                            "EXTRACT(HOUR FROM open_time) AS open, EXTRACT(HOUR FROM close_time) AS close FROM brands "
                            "JOIN locations ON b_id = brand_id "
                            "JOIN hours ON l_id = location_id "
                            "WHERE l_id = :l_id"), {"l_id": location_id})
        for location in locations:
            if not res:
                res.append({
                    "address": location.address,
                    "address_id": location.l_id,
                    "brand": location.name,
                    "brand_id": location.b_id,
                    "Hours": []
                })
            if location.open in (0, 24):
                open_time = "12 AM"
            elif location.open < 12:
                open_time = str(location.open) + " AM"
            elif location.open == 12:
                open_time = "12 PM"
            else:
                open_time = str(location.open - 12) + " PM"
                
            if location.close in (0, 24):
                close_time = "12 AM"
            elif location.close < 12:
                close_time = str(location.close) + " AM"
            elif location.close == 12:
                close_time = "12 PM"
            else:
                close_time = str(location.close - 12) + " PM"
                
            res[0]["Hours"].append({
                "Day": location.day_name,
                "open_time": open_time,
                "close_time": close_time
            })

    if not res:
        # raises bad input error on incorrect location or brand id
        raise HTTPException(status_code=400, detail="There is no such location")

    return res