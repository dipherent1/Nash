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


class SearchAppointment(BaseModel):
    phone: str
    date: Optional[str] = None


class CancelAppointment(BaseModel):
    appointment_id: str
    date: str
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
        "branches": [
            {
                "name": "Edmonds Office",
                "address": "23710 Edmonds Way, Edmonds, WA 98026",
                "phone": "(425) 697-5188",
                "days": ["Tuesday", "Thursday"],
                "available_time_slots": [
                    {"date": "2026-07-02", "time": "09:00 AM"},
                    {"date": "2026-07-02", "time": "10:00 AM"},
                    {"date": "2026-07-02", "time": "11:00 AM"},
                    {"date": "2026-07-02", "time": "12:00 PM"},
                    {"date": "2026-07-02", "time": "03:00 PM"},
                    {"date": "2026-07-02", "time": "04:00 PM"},
                    {"date": "2026-07-02", "time": "05:00 PM"},
                ],
            },
            {
                "name": "Lynnwood Office",
                "address": "5105 200th ST SW #110, Lynnwood, WA 98036",
                "phone": "(425) 771-2225",
                "days": ["Monday", "Wednesday", "Friday"],
                "available_time_slots": [
                    {"date": "2026-07-01", "time": "09:00 AM"},
                    {"date": "2026-07-01", "time": "10:00 AM"},
                    {"date": "2026-07-01", "time": "11:00 AM"},
                    {"date": "2026-07-01", "time": "12:00 PM"},
                    {"date": "2026-07-01", "time": "03:00 PM"},
                    {"date": "2026-07-01", "time": "04:00 PM"},
                    {"date": "2026-07-01", "time": "05:00 PM"},
                ],
            },
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


@app.post("/SearchAppointment")
async def search_appointment(item: SearchAppointment):
    # Search for appointments based on the provided phone and optional date
    mock_data = {
        "appointments": [
            {
                "appointment_id": 56789,
                "client_name": "John Doe",
                "client_phone": item.phone,  # Returning the parameter passed by the user
                "appointment_datetime": "2026-07-01T10:00:00",  # Example datetime
                "status": "confirmed",
            },
            {
                "appointment_id": 56790,
                "client_name": "John Doe",
                "client_phone": item.phone,  # Returning the parameter passed by the user
                "appointment_datetime": "2026-07-02T11:00:00",  # Example datetime
                "status": "pending",
            },
        ]
    }

    return mock_data


@app.post("/CancelAppointment")
async def cancel_appointment(item: CancelAppointment):
    # Cancel the appointment based on the provided appointment ID, date, and phone
    mock_data = {
        "cancellation_result": "success",
        "appointment_id": item.appointment_id,  # Returning the parameter passed by the user
        "date": item.date,  # Returning the parameter passed by the user
        "phone": item.phone,  # Returning the parameter passed by the user
    }

    return mock_data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
