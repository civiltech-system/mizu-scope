from fastapi import APIRouter

from app.api.v1 import regions, nearby, commercial_water

api_router = APIRouter()
api_router.include_router(regions.router, prefix="/regions", tags=["regions"])
api_router.include_router(nearby.router, prefix="/nearby", tags=["nearby"])
api_router.include_router(commercial_water.router, prefix="/commercial-water", tags=["commercial-water"])
