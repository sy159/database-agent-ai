import time

from fastapi import APIRouter, Request

from app.core.response import success

router = APIRouter()


@router.get("/index")
async def index(request: Request):
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.headers.get("X-Real-IP", request.client.host)
    return success({
        "timestamp": int(round(time.time() * 1000)),
        "client_ip": ip,
    })


@router.get("/healthz")
async def liveness():
    return success({"status": "ok"})


@router.get("/readyz")
async def readiness():
    # todo 检查依赖db、redis等 "status": "not ready"
    return success({"status": "ready"})
