import math

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.models import WaterRegion
from app.services.coffee_service import calc_coffee_score
from app.utils.hardness import get_water_type

router = APIRouter()

EARTH_RADIUS_KM = 6371.0


def haversine(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng / 2) ** 2
    return EARTH_RADIUS_KM * 2 * math.asin(math.sqrt(a))


@router.get("")
async def get_nearby(
    lat: float = Query(..., description="緯度"),
    lng: float = Query(..., description="経度"),
    radius_km: float = Query(50.0, description="検索半径 (km)"),
    limit: int = Query(10, le=50),
    db: AsyncSession = Depends(get_db),
):
    """現在地周辺の地域を距離順で返す"""
    lat_delta = radius_km / 111.0
    lng_delta = radius_km / (111.0 * abs(math.cos(math.radians(lat))) + 0.001)

    result = await db.execute(
        select(WaterRegion)
        .options(selectinload(WaterRegion.quality))
        .where(
            WaterRegion.lat.between(lat - lat_delta, lat + lat_delta),
            WaterRegion.lng.between(lng - lng_delta, lng + lng_delta),
        )
    )
    regions = result.scalars().all()

    items = []
    for region in regions:
        if region.lat is None or region.lng is None:
            continue
        dist = haversine(lat, lng, float(region.lat), float(region.lng))
        if dist > radius_km:
            continue
        q = region.quality
        hardness = float(q.hardness) if q and q.hardness is not None else None
        items.append({
            "id": region.id,
            "name": f"{region.prefecture or ''}{region.city or ''}".strip(),
            "slug": region.slug,
            "distance_km": round(dist, 2),
            "hardness": hardness,
            "water_type": get_water_type(hardness),
            "drinkable": q.drinkable if q else None,
            "coffee_score": calc_coffee_score(
                hardness,
                float(q.ph) if q and q.ph is not None else None,
                float(q.magnesium) if q and q.magnesium is not None else None,
            ) if hardness is not None else None,
        })

    items.sort(key=lambda x: x["distance_km"])
    return items[:limit]
