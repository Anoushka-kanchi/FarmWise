from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime


DATABASE_URL = "sqlite:///marketplace.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


Base = declarative_base()


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ==========================================
# FARMER CROP LISTING
# ==========================================

class CropListing(Base):

    __tablename__ = "crop_listings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    farmer_name = Column(
        String,
        nullable=False
    )

    crop = Column(
        String,
        nullable=False
    )

    category = Column(
        String
    )

    quantity = Column(
        Float,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    location = Column(
        String
    )

    description = Column(
        String
    )

    image_filename = Column(
        String
    )

    farmer_id = Column(
        String
    )

    date_listed = Column(
        DateTime,
        default=datetime.utcnow
    )


# ==========================================
# FARMING PRODUCT
# ==========================================

class FarmingProduct(Base):

    __tablename__ = "farming_products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    category = Column(
        String,
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )


Base.metadata.create_all(
    bind=engine
)