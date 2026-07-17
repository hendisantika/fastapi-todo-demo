from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from database import Base, SessionLocal
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session

import models,schemas, repositories
import logging

#create FastAPI application instance
app = FastAPI()

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally:
        db.close()

# Create routers for different route groups
todo_router_v1 = APIRouter(prefix="/todos", tags=["todos v1"])

'''
 -  Here we injected schemas / serializer from TodoRead to response since this can 
    show more than one todo result we put use list 
 -  We create a simple repository to perform database process here
 -  Last we put proper http status using status_code decorator.
    Common status codes in the status module:
    status.HTTP_200_OK (default for successful responses)
    status.HTTP_201_CREATED
    status.HTTP_204_NO_CONTENT
    status.HTTP_400_BAD_REQUEST
    status.HTTP_404_NOT_FOUND
    status.HTTP_500_INTERNAL_SERVER_ERROR

'''