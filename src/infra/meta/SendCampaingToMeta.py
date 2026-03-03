import os
import httpx
import logging
from fastapi import FastAPI
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

app = FastAPI()

TOKEN_META = os.getenv("TOKEN_META")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

logger = logging.getLogger(__name__)


async def send_campaing(data: Dict[str, Any]):
    payload = data.get("payload")
    phone_number_id = data.get("phone_number_id", PHONE_NUMBER_ID)
    categoria = data.get("category")

    type_message = "messages"
    if categoria == "marketing":
        type_message = "marketing_messages"

    url_meta = f"https://graph.facebook.com/v22.0/{phone_number_id}/{type_message}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN_META}"
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(
            url_meta,
            json=payload,
            headers=headers
        )

    return {
        data: response.json(),
        status: response.status_code
    }