"""Database connection handling using SQLAlchemy.

This module defines a global engine and session factory.  The database URL
should be provided via the `DATABASE_URL` environment variable.  When
running under Docker Compose, the default points at the `db` service.
"""

import os


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@db:5432/postgres",
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    """Yield a database session scoped to the current request.

    FastAPI will cleanly close the session after the response is returned.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
