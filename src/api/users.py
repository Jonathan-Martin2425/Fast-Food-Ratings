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


@router.delete("/")
def delete_user(user: UserDelete):
    username = user.username.strip()
    password = user.password.strip()

    # Prevent deletion of the 'Anonymous' user
    if username == "Anonymous":
        raise HTTPException(status_code=405, detail="Can't delete 'Anonymous' user and their reviews")

    with db.engine.begin() as connection:
        # Retrieve user details
        user_record = connection.execute(
            sqlalchemy.text("SELECT u_id, password FROM users WHERE name = :name"),
            {"name": username}
        ).fetchone()

        if not user_record:
            raise HTTPException(status_code=404, detail="User does not exist")

        # Verify the password
        stored_password = user_record.password
        if password != stored_password:
            raise HTTPException(status_code=403, detail="Incorrect password")

        # Delete reviews, visited records, and the user
        connection.execute(
            sqlalchemy.text("DELETE FROM reviews WHERE publisher_id = :user_id"),
            {"user_id": user_record.u_id}
        )
        connection.execute(
            sqlalchemy.text("DELETE FROM user_visits WHERE user_id = :user_id"),
            {"user_id": user_record.u_id}
        )
        connection.execute(
            sqlalchemy.text("DELETE FROM users WHERE u_id = :user_id"),
            {"user_id": user_record.u_id}
        )
    return {"message": f"User '{username}' and their associated data have been deleted successfully"}
