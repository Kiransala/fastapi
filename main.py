from typing import List
from models import User,Gender,Role,UserUpdateRequest
from uuid import UUID
from fastapi import FastAPI, HTTPException

app = FastAPI()

db: List[User] = [
  User(id=UUID("e77e1378-04b5-4372-8b5c-5c058cd0bda7"), first_name="kiran",last_name="sala", gender=Gender.male,roles=[Role.admin,Role.student] ),
  User(id=UUID("2c695103-4c68-429e-b4c0-7ecee040665c"), first_name="karan",last_name="patel", gender=Gender.male,roles=[Role.student] ),
  User(id=UUID("8a81af7b-cf01-49c6-ae51-8f33d6d056c6"), first_name="haris",last_name="khan", gender=Gender.male,roles=[Role.student] )
]

@app.get('/')
async def root():
  return {"Hello":"Mundo"}

@app.get('/api/v1/users')
async def fetch_users():
  return db;

@app.post('/api/v1/users')
async def register_user(user: User):
  db.append(user)
  return {"id":user.id}

@app.delete('/api/v1/users/{user_id}')
async def delete_user(user_id:UUID):
  for user in db:
    if user.id ==user_id:
      db.remove(user)
      return
  raise HTTPException(
    status_code=404,
    detail=F"user with id: {user_id} does not exists"
  )

@app.put('/api/v1/users/{user_id}')
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
  for user in db:
    if user.id == user_id:
      if user_update.first_name is not None:
        user.first_name = user_update.first_name
      if user_update.last_name is not None:
        user.last_name = user_update.last_name 
      if user_update.middle_name is not None:
        user.middle_name = user_update.middle_name
      if user_update.roles is not None:
        user.roles = user_update.roles
      return
  raise HTTPException(
    status_code=404,
    detail=F"user with id: {user_id} does not exists"
  )