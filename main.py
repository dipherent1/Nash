from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI()


class SearchClient(BaseModel):
    phone: str


@app.post("/SearchClient")
async def submit_item(item: SearchClient):
    mock_data = {
        "record_found": True,
        "user_id": 10293,
        "name": "John Doe",
        "phone": item.phone,  # Returning the parameter passed by the user
        "email": "johndoe@example.com",
        "status": "active",
        "membership_tier": "Premium",
    }

    return mock_data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
