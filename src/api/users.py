from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(auth.get_api_key)],
)


class Username(BaseModel):
    username: str
    
class UserCreate(BaseModel):
    username: str
    password: str

class UserDelete(BaseModel):
    username: str
    password: str


@router.post("/signup", status_code=201)
def add_user(user: UserCreate):
    actualUname = user.username.strip()
    password = user.password.strip()

    # Validate username and password length
    if len(actualUname) >= 30:
        raise HTTPException(status_code=400, detail="Username too long, max 30 characters")
    elif len(actualUname) <= 4:
        raise HTTPException(status_code=400, detail="Username too short, min 4 characters")
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password too short, min 6 characters")

    with db.engine.begin() as connection:
        # Check if username already exists
        t = connection.execute(sqlalchemy.text("SELECT name FROM users"))
        for name in t:
            if name.name == actualUname:
                raise HTTPException(status_code=400, detail="Username already exists")

        # Insert the new user with username and plain password
        u_id = connection.execute(
            sqlalchemy.text(
                "INSERT INTO users (name, password) VALUES (:name, :password) RETURNING u_id"
            ),
            {"name": actualUname, "password": password},
        ).scalar()
        return {"id": u_id}


@router.get("/")
def get_users():
    res = []
    with db.engine.begin() as connection:
        users = connection.execute(sqlalchemy.text("SELECT u_id, name FROM users "
                                                   "ORDER BY created_at ASC"))
        for user in users:
            res.append({
                "name": user.name,
                "id": user.u_id
            })
    return res


@router.get("/{username}")
def get_user_reviews(username: str):
    res = []
    with db.engine.begin() as connection:
        reviews = connection.execute(sqlalchemy.text(
            "SELECT date_published, name, service_rating, quality_rating, cleanliness_rating, description, u_id FROM reviews "
            "JOIN users ON publisher_id = u_id "
            "WHERE name = :name"), {"name": username})
        # iterates through reviews and adds each one to response
        for review in reviews:
            res.append({
                "publisher": review.name,
                "description": review.description,
                "ratings (S, Q, C)": [review.service_rating, review.quality_rating, review.cleanliness_rating],
                "date_published": review.date_published,
                "publisher_id": review.u_id
            })
        if len(res) == 0:
            res.append({"message": "There are no reviews from this user or user does not exist."})
    return res


@router.delete(("/"))
def delete_user(username: Username):
    if username.username.strip() == "Anonymous":
        raise HTTPException(status_code=405, detail="Can't delete 'Anonymous' user and their reviews")

    with db.engine.begin() as connection:
        t = connection.execute(sqlalchemy.text("SELECT name, r_id FROM users "
                                               "JOIN reviews ON u_id = publisher_id "
                                               "WHERE :name = name"), {"name": username.username})

        reviews = []
        for r in t:
            reviews.append({
                "id": r.r_id
            })

        if len(reviews) > 0:
            connection.execute(sqlalchemy.text("DELETE FROM reviews WHERE :id = r_id"), reviews)
            connection.execute(sqlalchemy.text("DELETE FROM visited WHERE :id = user_id"), username.username)
        connection.execute(sqlalchemy.text("DELETE FROM users WHERE :name = name"), {"name": username.username})
    return []
