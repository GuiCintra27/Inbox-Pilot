from fastapi import APIRouter

from app.api.analyze import router as analyze_router
from app.api.ops import router as ops_router

router = APIRouter()
router.include_router(analyze_router)
router.include_router(ops_router)
