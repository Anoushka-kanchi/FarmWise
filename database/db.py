from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create database engine
engine = create_engine('sqlite:///farmwise.db')

# Create base class for models
Base = declarative_base()

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class CropListing(Base):
    __tablename__ = "crop_listings"

    id = Column(Integer, primary_key=True, index=True)
    farmer_name = Column(String, index=True, nullable=False)
    crop = Column(String, nullable=False)
    category = Column(String)
    price = Column(Float)
    quantity = Column(Float)
    location = Column(String)
    description = Column(String)
    image_filename = Column(String)
    farmer_id = Column(String)
    date_listed = Column(DateTime, default=datetime.utcnow)


class FarmingProduct(Base):
    __tablename__ = "farming_products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    category = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    farmer_id = Column(String)
    date_listed = Column(DateTime, default=datetime.utcnow)
