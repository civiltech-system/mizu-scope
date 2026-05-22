from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class WaterRegion(Base):
    __tablename__ = "water_region"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    country_code: Mapped[str] = mapped_column(String(3), nullable=False, index=True)
    prefecture: Mapped[str | None] = mapped_column(String(100))
    city: Mapped[str | None] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(200), nullable=False, unique=True, index=True)
    lat: Mapped[float | None] = mapped_column(Numeric(10, 7))
    lng: Mapped[float | None] = mapped_column(Numeric(10, 7))
    population: Mapped[int | None] = mapped_column(BigInteger)
    water_source: Mapped[str | None] = mapped_column(String(200))
    utility_name: Mapped[str | None] = mapped_column(String(200))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    quality: Mapped["WaterQuality | None"] = relationship(
        "WaterQuality", back_populates="region", uselist=False
    )
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="region")


class WaterQuality(Base):
    __tablename__ = "water_quality"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    region_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("water_region.id", ondelete="CASCADE"), index=True
    )
    hardness: Mapped[float | None] = mapped_column(Numeric(8, 2))
    ph: Mapped[float | None] = mapped_column(Numeric(4, 2))
    calcium: Mapped[float | None] = mapped_column(Numeric(8, 2))
    magnesium: Mapped[float | None] = mapped_column(Numeric(8, 2))
    sodium: Mapped[float | None] = mapped_column(Numeric(8, 2))
    tds: Mapped[float | None] = mapped_column(Numeric(8, 2))
    chlorine: Mapped[float | None] = mapped_column(Numeric(6, 3))
    drinkable: Mapped[bool] = mapped_column(Boolean, default=True)
    boil_recommended: Mapped[bool] = mapped_column(Boolean, default=False)
    confidence_score: Mapped[str] = mapped_column(String(20), default="official")
    source_url: Mapped[str | None] = mapped_column(String(500))
    measured_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    region: Mapped["WaterRegion"] = relationship("WaterRegion", back_populates="quality")


class CommercialWater(Base):
    __tablename__ = "commercial_water"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    country_code: Mapped[str | None] = mapped_column(String(3))
    water_source: Mapped[str | None] = mapped_column(String(200))
    hardness: Mapped[float | None] = mapped_column(Numeric(8, 2))
    ph: Mapped[float | None] = mapped_column(Numeric(4, 2))
    calcium: Mapped[float | None] = mapped_column(Numeric(8, 2))
    magnesium: Mapped[float | None] = mapped_column(Numeric(8, 2))
    sodium: Mapped[float | None] = mapped_column(Numeric(8, 2))
    tds: Mapped[float | None] = mapped_column(Numeric(8, 2))
    water_type: Mapped[str | None] = mapped_column(String(20))
    coffee_score: Mapped[int | None] = mapped_column(Integer)
    image_url: Mapped[str | None] = mapped_column(String(500))
    source_url: Mapped[str | None] = mapped_column(String(500))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    region_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("water_region.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[str] = mapped_column(String(128), nullable=False)
    rating: Mapped[int | None] = mapped_column(Integer)
    taste_comment: Mapped[str | None] = mapped_column(Text)
    coffee_match: Mapped[int | None] = mapped_column(Integer)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    region: Mapped["WaterRegion"] = relationship("WaterRegion", back_populates="reviews")
