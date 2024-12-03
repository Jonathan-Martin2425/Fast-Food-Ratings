from fastapi import FastAPI, exceptions, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.api import brands, reviews, users, locations, ingredients

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
app.include_router(ingredients.router)
app.include_router(locations.router)


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
# shows opening message
@app.get("/")
async def root():
    res = [{"message": "Welcome to Fast-Food-Ratings, for all your fast food needs."}]
    return res
