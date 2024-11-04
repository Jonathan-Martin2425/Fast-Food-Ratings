from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import endpoints
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
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Lucas Pierce",
        "email": "lupierce@calpoly.edu",
    },
)

app.include_router(endpoints.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)


"""
root of the website
shows opening message and all brands with their locations
"""
@app.get("/")
async def root():
    res = []
    with db.engine.begin() as connection:
        brands = connection.execute(sqlalchemy.text("SELECT address, name FROM brands "
                                                    "JOIN locations ON b_id = brand_id"))

    for b in brands:
        brand = {
            "brand": b.name,
            "addresses": []
        }

        bIsThere = False
        for cur in res:
            if cur["brand"] == b.name:
                bIsThere = True
        if not bIsThere:
            res.append(brand)

        for cur in res:
            if b.address not in cur["addresses"] and b.name == cur["brand"]:
                cur["addresses"].append(b.address)
    res.insert(0, {"message": "Welcome to Fast-Food-Ratings, for all your fast food needs."})

    return res