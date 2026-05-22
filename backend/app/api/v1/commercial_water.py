from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.cache import cache_get, cache_set, make_cache_key
from app.models.models import CommercialWater, WaterQuality

router = APIRouter()


def _fmt(w: CommercialWater) -> dict:
    return {
        "id": w.id,
        "name": w.name,
        "brand": w.brand,
        "country_code": w.country_code,
        "water_source": w.water_source,
        "hardness": float(w.hardness) if w.hardness is not None else None,
        "ph": float(w.ph) if w.ph is not None else None,
        "calcium": float(w.calcium) if w.calcium is not None else None,
        "magnesium": float(w.magnesium) if w.magnesium is not None else None,
        "sodium": float(w.sodium) if w.sodium is not None else None,
        "tds": float(w.tds) if w.tds is not None else None,
        "water_type": w.water_type,
        "coffee_score": w.coffee_score,
        "image_url": w.image_url,
    }


@router.get("")
async def list_commercial_water(
    water_type: str | None = Query(None, description="soft/medium/hard/very_hard"),
    db: AsyncSession = Depends(get_db),
):
    """市販ミネラルウォーター一覧"""
    cache_key = make_cache_key("commercial", water_type or "all")
    cached = await cache_get(cache_key)
    if cached:
        return cached

    query = select(CommercialWater).order_by(CommercialWater.hardness)
    if water_type:
        query = query.where(CommercialWater.water_type == water_type)

    result = await db.execute(query)
    waters = result.scalars().all()
    data = [_fmt(w) for w in waters]
    await cache_set(cache_key, data, ttl=86400)
    return data


@router.get("/match/{region_id}")
async def match_commercial_water(region_id: int, db: AsyncSession = Depends(get_db)):
    """地域の水道水硬度に近い市販水を上位3件提案"""
    cache_key = make_cache_key("commercial", "match", str(region_id))
    cached = await cache_get(cache_key)
    if cached:
        return cached

    result = await db.execute(
        select(WaterQuality.hardness).where(WaterQuality.region_id == region_id)
    )
    hardness = result.scalar_one_or_none()
    if hardness is None:
        raise HTTPException(status_code=404, detail="Region quality data not found")

    result = await db.execute(
        select(CommercialWater)
        .order_by(func.abs(CommercialWater.hardness - hardness))
        .limit(3)
    )
    waters = result.scalars().all()
    data = [_fmt(w) for w in waters]
    await cache_set(cache_key, data, ttl=21600)
    return data


@router.get("/{water_id}")
async def get_commercial_water(water_id: int, db: AsyncSession = Depends(get_db)):
    """市販水詳細"""
    cache_key = make_cache_key("commercial", "id", str(water_id))
    cached = await cache_get(cache_key)
    if cached:
        return cached

    result = await db.execute(select(CommercialWater).where(CommercialWater.id == water_id))
    water = result.scalar_one_or_none()
    if not water:
        raise HTTPException(status_code=404, detail="Not found")

    data = _fmt(water)
    await cache_set(cache_key, data, ttl=86400)
    return data
