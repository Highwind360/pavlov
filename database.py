"""
database.py
highwind

Configuration for sqlalchemy
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from .settings import DATABASE_URL


Base = declarative_base()
Session = sessionmaker()


# TODO: on both tables, the date created
# TODO: apply constraints to the columns

class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key = True)
    name = Column(String)
    value = Column(Integer)
    goal = Column(Integer)

    exercise_sets = relationship("ExerciseSet", back_populates="exercise",
        cascade="all, delete, delete-orphan")


class ExerciseSet(Base):
    __tablename__ = "exercise_sets"
    id = Column(Integer, primary_key = True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    reps = Column(Integer)

    exercise = relationship("Exercise", back_populates="exercise_sets")


engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine) # create uncreated tables
Session.configure(bind=engine)
