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
