from fastapi import APIRouter, HTTPException, Depends
from app.auth import verify_jwt_token
from app.config import settings
import requests
import json
from loguru import logger

api_router = APIRouter()


@api_router.post("/api/check-imei")
async def protected_route(deviceId: str, headers: dict = Depends(verify_jwt_token)):
    logger.info("я сработал")
    url = "https://api.imeicheck.net/v1/checks"

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {settings.IMEI_CHECK_TOKEN}",
            "Accept-Language": "en",
        },
        data={"deviceId": deviceId, "serviceId": '1'},
    )
    return response.json() 
