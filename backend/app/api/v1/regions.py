from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.cache import cache_get, cache_set, make_cache_key
from app.models.models import WaterRegion
from app.services.coffee_service import calc_coffee_score
from app.utils.hardness import get_water_type

router = APIRouter()


def _region_to_dict(region: WaterRegion) -> dict:
    q = region.quality
    hardness = float(q.hardness) if q and q.hardness is not None else None
    ph = float(q.ph) if q and q.ph is not None else None
    magnesium = float(q.magnesium) if q and q.magnesium is not None else None
    coffee_score = calc_coffee_score(hardness, ph, magnesium) if hardness is not None else None
    water_type = get_water_type(hardness)

    return {
        "id": region.id,
        "country_code": region.country_code,
        "prefecture": region.prefecture,
        "city": region.city,
        "slug": region.slug,
        "lat": float(region.lat) if region.lat is not None else None,
        "lng": float(region.lng) if region.lng is not None else None,
        "population": region.population,
        "water_source": region.water_source,
        "utility_name": region.utility_name,
        "coffee_score": coffee_score,
        "water_type": water_type,
        "quality": {
            "hardness": hardness,
            "ph": ph,
            "calcium": float(q.calcium) if q and q.calcium is not None else None,
            "magnesium": magnesium,
            "sodium": float(q.sodium) if q and q.sodium is not None else None,
            "tds": float(q.tds) if q and q.tds is not None else None,
            "chlorine": float(q.chlorine) if q and q.chlorine is not None else None,
            "drinkable": q.drinkable if q else True,
            "boil_recommended": q.boil_recommended if q else False,
            "confidence_score": q.confidence_score if q else "estimated",
            "measured_at": q.measured_at.isoformat() if q and q.measured_at else None,
        } if q else None,
    }


@router.get("")
async def get_regions_geojson(db: AsyncSession = Depends(get_db)):
    """地図マーカー用 GeoJSON 形式で全地域を返す"""
    cache_key = make_cache_key("regions", "geojson")
    cached = await cache_get(cache_key)
    if cached:
        return cached

    result = await db.execute(
        select(WaterRegion).options(selectinload(WaterRegion.quality)).order_by(WaterRegion.id)
    )
    regions = result.scalars().all()

    features = []
    for region in regions:
        if region.lat is None or region.lng is None:
            continue
        name = f"{region.prefecture or ''}{region.city or ''}".strip()
        q = region.quality
        hardness = float(q.hardness) if q and q.hardness is not None else None
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(region.lng), float(region.lat)],
            },
            "properties": {
                "id": region.id,
                "name": name,
                "slug": region.slug,
                "hardness": hardness,
                "water_type": get_water_type(hardness),
                "drinkable": q.drinkable if q else None,
                "coffee_score": calc_coffee_score(
                    hardness,
                    float(q.ph) if q and q.ph is not None else None,
                    float(q.magnesium) if q and q.magnesium is not None else None,
                ) if hardness is not None else None,
            },
        })

    geojson = {"type": "FeatureCollection", "features": features}
    await cache_set(cache_key, geojson, ttl=3600)
    return geojson


@router.get("/slug/{slug:path}")
async def get_region_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    """slug 指定で地域詳細を返す"""
    cache_key = make_cache_key("regions", "slug", slug)
    cached = await cache_get(cache_key)
    if cached:
        return cached

    result = await db.execute(
        select(WaterRegion).options(selectinload(WaterRegion.quality)).where(WaterRegion.slug == slug)
    )
    region = result.scalar_one_or_none()
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    data = _region_to_dict(region)
    await cache_set(cache_key, data, ttl=21600)
    return data


@router.get("/{region_id}")
async def get_region(region_id: int, db: AsyncSession = Depends(get_db)):
    """ID 指定で地域詳細を返す"""
    cache_key = make_cache_key("regions", "id", str(region_id))
    cached = await cache_get(cache_key)
    if cached:
        return cached

    result = await db.execute(
        select(WaterRegion).options(selectinload(WaterRegion.quality)).where(WaterRegion.id == region_id)
    )
    region = result.scalar_one_or_none()
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")

    data = _region_to_dict(region)
    await cache_set(cache_key, data, ttl=21600)
    return data
