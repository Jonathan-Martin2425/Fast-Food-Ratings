from fastapi import FastAPI, exceptions, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import brands, reviews, users
import sqlalchemy
from src import database as db
import json
import logging
import sys

description = """
Fast-Food-Ratings shows you what others think about different food brands and their locations
"""

app = FastAPI(
    title="Fast-Food-Ratings",
    description=description,
    version="0.0.1",
    contact={
        "name": "Jonathan Martin",
        "email": "jmart663@calpoly.edu",
    },
)

app.include_router(brands.router)
app.include_router(reviews.router)
app.include_router(users.router)


@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)


# root of the website
# shows opening message and all brands with their locations
@app.get("/")
async def root():
    res = []

    # gets all brands and their locations
    try:
        with db.engine.begin() as connection:
            brands = connection.execute(sqlalchemy.text("SELECT b_id, l_id, address, name FROM brands "
                                                        "JOIN locations ON b_id = brand_id "
                                                        "ORDER BY name ASC, l_id ASC"))
    except BaseException as e:
        print(e.args[0])
        raise HTTPException(status_code=503, detail="Server unable to access appropriate data")

    # iterates through each location to add them to response
    brands_dict = {}
    for b in brands:
        brand = {
            "brand": b.name,
            "brand_id": b.b_id,
            "addresses": []
        }

        try:
            # adds address to brand
            brands_dict[b.name]["addresses"].append({"address": b.address,
                                                    "address_id": b.l_id})
        except KeyError:
            # checks if brand already exists in response
            # and if it doesn't, adds it
            brands_dict[b.name] = brand
            brands_dict[b.name]["addresses"].append({"address": b.address,
                                                     "address_id": b.l_id})

    # converts dictionary to list of dictionaries for better JSON format
    for key in brands_dict:
        res.append(brands_dict[key])

    # adds opening message to start of response
    res.insert(0, {"message": "Welcome to Fast-Food-Ratings, for all your fast food needs."})

    return res
