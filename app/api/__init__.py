from fastapi import APIRouter
from app.api.endpoints import root

api_router = APIRouter()

# 根接口，不加前缀
api_router.include_router(root.router, tags=["root"])
