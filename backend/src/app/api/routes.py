from fastapi import APIRouter

from app.api.analyze import router as analyze_router

router = APIRouter()
router.include_router(analyze_router)
