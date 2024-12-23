from fastapi import FastAPI, APIRouter
from routers.user import user_router as api_v1

router = APIRouter(
    prefix="/api/v1",
)
router.include_router(api_v1)
app = FastAPI()
app.include_router(router)
