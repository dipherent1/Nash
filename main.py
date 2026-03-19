from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI()


class SearchClient(BaseModel):
    phone: str


class CreateUser(BaseModel):
    client_first_name: str
    client_last_name: str
    client_phone: str


class BookAppointment(BaseModel):
    client_first_name: str
    appointment_datetime: str
    client_last_name: str
    client_phone: str
    client_branch: str


class ValidateAppointment(BaseModel):
    date: str
    branch: str


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


@app.post("/CreateClient")
async def create_user(item: CreateUser):
    mock_data = {
        "created successfully": True,
        "user_id": 10293,
        "name": f"{item.client_first_name} {item.client_last_name}",
        "phone": item.client_phone,  # Returning the parameter passed by the user
        "email": "johndoe@example.com",
        "status": "active",
        "membership_tier": "Premium",
    }

    return mock_data


@app.post("/CheckAvailability")
async def check_availability():
    # get available time slots for the user
    mock_data = {
        "available_time_slots": [
            {"date": "2026-07-01", "time": "10:00 AM"},
            {"date": "2026-07-01", "time": "11:00 AM"},
            {"date": "2026-07-01", "time": "02:00 PM"},
        ]
    }

    return mock_data


@app.post("/BookAppointment")
async def book_appointment(item: BookAppointment):
    mock_data = {
        "appointment_booked": True,
        "appointment_id": 56789,
        "client_name": f"{item.client_first_name} {item.client_last_name}",
        "client_phone": item.client_phone,  # Returning the parameter passed by the user
        "appointment_datetime": item.appointment_datetime,  # Returning the parameter passed by the user
        "status": "confirmed",
    }

    return mock_data


@app.post("/Validate")
async def validate_appointment(item: ValidateAppointment):
    # Validate the appointment based on the provided date and branch
    mock_data = {
        "validation_result": "valid",
        "date": item.date,  # Returning the parameter passed by the user
        "branch": item.branch,  # Returning the parameter passed by the user
    }

    return mock_data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
