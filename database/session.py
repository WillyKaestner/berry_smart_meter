"""Create a connection to database and set up a database session"""
from contextlib import contextmanager
import logging
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from settings import SETTINGS

# Get logger
logger = logging.getLogger(__name__)

# Define global SQLAlchemy Database engine
engine = None


def setup_db(pool_size: int = 2, max_overflow: int = 1):
    global engine
    engine = create_db_engine(pool_size=pool_size, max_overflow=max_overflow)


def create_db_engine(alembic_use: bool = False, pool_size: int = 1, max_overflow: int = 0):
    sqlalchemy_database_url = f"postgresql://{SETTINGS.database_username}:{SETTINGS.database_password}@" \
                              f"{SETTINGS.database_host}:5432/{SETTINGS.database_name}"
    if alembic_use is True:
        return sqlalchemy_database_url

    # Create and return a SQLAlchemy engine for database connections.
    engine_created = create_engine(
        sqlalchemy_database_url, poolclass=QueuePool, pool_size=pool_size, max_overflow=max_overflow
    )
    return engine_created


@contextmanager  # decorator to make this function a context manager without manually adding __enter__() and __exit__()
def get_db() -> Session:
    """
    Creates a database session and returns it, while still closing the database session if an error occurs.
    Should be used as a context manager, e.g.:

    with get_db() as db:
        # do stuff with db

    Returns:
        SQLAlchemy Database session
    """
    # Set up a session factory with manual commit and flush control, bound to the engine.
    sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create a new database session.
    db = sessionlocal()

    # Yield the database session to the caller.
    try:
        yield db

    # Close the database session if it was successfully created, to prevent resource leaks.
    finally:
        db.close()
