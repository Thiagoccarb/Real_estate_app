from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": False}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(VARCHAR(45), nullable=True)
    email = Column(VARCHAR(45), nullable=False, unique=True)
    password = Column(VARCHAR(128), nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=True, default=None)


class Property(Base):
    __tablename__ = "properties"
    __mapper_args__ = {"eager_defaults": False}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(VARCHAR(45), nullable=True)
    image_ids = relationship("Image", backref="property")
    action = Column(VARCHAR(45), nullable=True)
    type = Column(VARCHAR(45), nullable=True)
    address_id = Column(Integer, ForeignKey("addresses.id", ondelete="CASCADE"))
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=True, default=None)


class Image(Base):
    __tablename__ = "images"
    __mapper_args__ = {"eager_defaults": False}

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(VARCHAR(512), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id", ondelete="CASCADE"))
    created_at = Column(DateTime, server_default=func.current_timestamp())
    audio_hash = Column(VARCHAR(512), nullable=True)
    position = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)


class City(Base):
    __tablename__ = "cities"
    __mapper_args__ = {"eager_defaults": False}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(VARCHAR(512), nullable=False)
    state = Column(VARCHAR(8), nullable=False)


class Address(Base):
    __tablename__ = "addresses"
    __mapper_args__ = {"eager_defaults": False}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    street_name = Column(VARCHAR(512), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"))
    number = Column(VARCHAR(45), nullable=True)
    cep = Column(VARCHAR(45), nullable=False)
