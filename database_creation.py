# # database_creation.py
#
# from sqlalchemy import create_engine, Column, Integer, String, DateTime, Time, Float, Boolean
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# # Define the database engine
# engine = create_engine('sqlite:///allocations_db/test.db')
#
# # Define the base class for declarative models
# Base = declarative_base()
#
#
# # Define the StaffTable class
# class StaffTable(Base):
#     __tablename__ = 'staff_table'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100))
#     role = Column(String(100))
#     gender = Column(String(20))
#     assigned = Column(Boolean, default=False)
#     start_time = Column(Integer, default=0)
#     end_time = Column(Integer, default=12)
#
#     def __init__(self, name, role, gender, assigned, start_time, end_time):
#         self.name = name
#         self.role = role
#         self.gender = gender
#         self.assigned = assigned
#         self.start_time = start_time
#         self.end_time = end_time
#
#     def as_dict(self):
#         return {h.name: getattr(self, h.name) for h in self.__table__.columns}
#
#
# # Define the ObservationsTable class
# class ObservationsTable(Base):
#     __tablename__ = 'patient_table'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100))
#     observation_level = Column(Integer, default=0)
#     room_number = Column(String(100))
#     gender_req = Column(String(20), default=None)
#
#     def as_dict(self):
#         return {h.name: getattr(self, h.name) for h in self.__table__.columns}
#
#
# # Create the tables in the database
# Base.metadata.create_all(engine)
# database_creation.py

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Time, Float, Boolean, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import sessionmaker

# Define the database engine
engine = create_engine('sqlite:///allocations_db/test.db')

# Define the base class for declarative models
Base = declarative_base()


# Define the StaffTable class
class StaffTable(Base):
    __tablename__ = 'staff_table'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    role = Column(String(100))
    gender = Column(String(20))
    assigned = Column(Boolean, default=False)
    start_time = Column(Integer, default=0)
    end_time = Column(Integer, default=12)
    duration = Column(Integer)

    def __init__(self, name, role, gender, assigned, start_time, end_time, duration):
        self.name = name
        self.role = role
        self.gender = gender
        self.assigned = assigned
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Define the ObservationsTable class
class ObservationsTable(Base):
    __tablename__ = 'patient_table'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    observation_level = Column(Integer, default=0)
    room_number = Column(String(100))
    gender_req = Column(String(20), default=None)
    omit_staff = Column(MutableList.as_mutable(PickleType), default=[])

    def __init__(self, name, observation_level, room_number, gender_req=None, omit_staff=None):
        self.name = name
        self.observation_level = observation_level
        self.room_number = room_number
        self.gender_req = gender_req
        self.omit_staff = omit_staff or []

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Create the tables in the database
Base.metadata.create_all(engine)
