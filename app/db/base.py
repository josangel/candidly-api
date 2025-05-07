"""Base model for SQLAlchemy ORM."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all models in the application.
    This class is used to define the base for all models using SQLAlchemy.
    """

    pass
