import os
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The connection is configured from environment variables so no credentials are
# committed to source control. Either set a full DB_URL, or set the individual
# DB_* parts below and the MySQL URL is assembled for you.
#
#   export DB_URL="mysql+mysqlconnector://user:password@host:3306/todos"
# or
#   export DB_USER=root DB_PASSWORD=secret DB_HOST=127.0.0.1 DB_PORT=3306 DB_NAME=todos
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "todos")

# quote_plus keeps special characters in the password from breaking the URL.
DB_URL = os.getenv(
    "DB_URL",
    f"mysql+mysqlconnector://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

# Initialize database engine (MySQL). pool_pre_ping avoids stale-connection errors.
engine = create_engine(DB_URL, echo=True, pool_pre_ping=True)

# Create a session factory bound to the engine
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

# Create the base class for all ORM models
# The Base object serves as the parent for all database models you define in your application.
Base = declarative_base()