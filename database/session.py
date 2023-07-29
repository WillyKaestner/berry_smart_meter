"""Create a connection to database and set up a database session"""

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import SETTINGS


def create_db_engine(alembic_use: bool = False):
    sqlalchemy_database_url = f"postgresql://{SETTINGS.database_username}:{SETTINGS.database_password}@" \
                              f"{SETTINGS.database_host}:5432/{SETTINGS.database_name}"
    if alembic_use is True:
        return sqlalchemy_database_url

    engine = create_engine(sqlalchemy_database_url)
    return engine


def get_db() -> Session:
    """
    Creates a database session and returns it, while still closing the database session if an error occurs.

    We put the creation of the sessionlocal() and handling of the requests in a try block. And then we close it in the
    "finally" block. This way we make sure the database session is always closed after the request. Even if there was
    an exception while processing the request.

    Returns:
        SQLAlchemy Database session
    """
    engine = create_db_engine()
    sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = sessionlocal()
    try:
        return db
    finally:
        db.close()
