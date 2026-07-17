import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Read the database URL from the environment so the app runs out of the box.
# Defaults to a local SQLite file for the demo; set DB_URL to point at MySQL, e.g.
#   DB_URL="mysql+mysqlconnector://USER:PASSWORD@HOST:PORT/DB_NAME"
DB_URL = os.getenv("DB_URL", "sqlite:///./todos.db")

# SQLite needs check_same_thread disabled to be used across FastAPI's threads.
connect_args = {"check_same_thread": False} if DB_URL.startswith("sqlite") else {}

# Initialize database engine
engine = create_engine(DB_URL, echo=True, connect_args=connect_args)

# Create a session factory bound to the engine
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

# Create the base class for all ORM models
# The Base object serves as the parent for all database models you define in your application.
Base = declarative_base()