from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from shared.database.client import Base

class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False, unique=True)
    
    # Relationships
    subcategories = relationship("Subcategory", back_populates="category", cascade="all, delete")
    recordings = relationship("Recording", back_populates="category")


class Subcategory(Base):
    __tablename__ = "subcategory"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"))

    # Relationships
    category = relationship("Category", back_populates="subcategories")
    recordings = relationship("Recording", back_populates="subcategory")


class Company(Base):
    """Only used for interview recordings."""
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False, unique=True)
    
    # Relationships
    recordings = relationship("Recording", back_populates="company")


class Recording(Base):
    __tablename__ = "recording"

    id = Column(String, primary_key=True, index=True)
    s3_key_raw = Column(String, nullable=False)
    s3_key_merged = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    recording_ended_at = Column(DateTime, nullable=False)
    details = Column(Text, nullable=True)  # Optional details
    status = Column(String, default="unprocessed", nullable=True)
    duration = Column(Integer, nullable=True)  # Duration in seconds

    # Foreign keys
    category_id = Column(Integer, ForeignKey("category.id", ondelete="SET NULL"), nullable=True)
    subcategory_id = Column(Integer, ForeignKey("subcategory.id", ondelete="SET NULL"), nullable=True)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    category = relationship("Category", back_populates="recordings")
    subcategory = relationship("Subcategory", back_populates="recordings")
    company = relationship("Company", back_populates="recordings")
