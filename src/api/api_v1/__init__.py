from fastapi import APIRouter

from src.core.config import settings
from src.api.api_v1.routers.common import router as common_router
from src.api.api_v1.routers.wallet import router as wallet_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    common_router,
    prefix=settings.api.v1.common,
)

router.include_router(wallet_router, prefix=settings.api.v1.wallet)
