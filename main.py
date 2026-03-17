from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime, timedelta
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Appointment API",
    description="A simple API for managing appointments with mock data.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Mock Data
# Appointments: {appointment_id: {"phone": "123456", "date": "2026-03-20", "time": "10:00"}}
appointments = {}
appointment_counter = 1


# Models
class PhoneRequestBody(BaseModel):
    phone_number: str = "123-456-7890"


# Endpoints
@app.get(
    "/get_available_appointment",
    summary="Get Available Appointments",
    description="Retrieve available appointment slots for a specific day or a date range.",
)
async def get_available_appointment(
    target_date: Optional[date] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    """
    Get available appointments.
    - If target_date is provided, returns two slots for that day.
    - If start_date and end_date are provided, returns one slot for that range.
    """
    results = []

    if target_date:
        # Specific day: make two
        slot1 = {"date": target_date.isoformat(), "time": "09:00", "available": True}
        slot2 = {"date": target_date.isoformat(), "time": "14:00", "available": True}
        results = [slot1, slot2]
        logger.info(f"Retrieved 2 slots for specific day: {target_date}")

    elif start_date and end_date:
        # Range: make one (e.g., middle of the range)
        mid_date = start_date + (end_date - start_date) / 2
        slot = {"date": mid_date.isoformat(), "time": "11:00", "available": True}
        results = [slot]
        logger.info(f"Retrieved 1 slot for range: {start_date} to {end_date}")

    else:
        # Default: if nothing provided, return a sample
        today = date.today()
        results = [{"date": today.isoformat(), "time": "10:00", "available": True}]
        logger.info("Retrieved default slot")

    for res in results:
        logger.info(f"Slot: {res}")

    return results


@app.post(
    "/make_appointment",
    summary="Make a New Appointment",
    description="Create a new appointment entry using a user's phone number.",
)
async def make_appointment(body: PhoneRequestBody):
    """
    Create an appointment using phone number.
    """
    global appointment_counter
    new_id = appointment_counter
    appointments[new_id] = {
        "phone_number": body.phone_number,
        "date": (date.today() + timedelta(days=1)).isoformat(),
        "time": "10:00",
    }
    appointment_counter += 1
    logger.info(f"Created appointment for: {body.phone_number} (ID: {new_id})")
    return {
        "message": "Appointment created",
        "id": new_id,
        "details": appointments[new_id],
    }


@app.post(
    "/update_appointment",
    summary="Update Existing Appointment",
    description="Update an existing appointment's details by searching for the user's phone number.",
)
async def update_appointment(body: PhoneRequestBody):
    """
    Update appointment using phone number.
    In this mock, we just find the first one with this phone and 'refresh' it.
    """
    found_id = None
    for app_id, details in appointments.items():
        if details["phone_number"] == body.phone_number:
            found_id = app_id
            break

    if not found_id:
        logger.warning(
            f"Update failed: No appointment found for phone {body.phone_number}"
        )
        raise HTTPException(
            status_code=404, detail="No appointment found for this phone number"
        )

    # Just update the time as a 'mock' update
    appointments[found_id]["time"] = "15:30"
    logger.info(f"Updated appointment ID {found_id} for phone: {body.phone_number}")
    return {
        "message": "Appointment updated",
        "id": found_id,
        "details": appointments[found_id],
    }


@app.post(
    "/cancel_appointment",
    summary="Cancel Appointment",
    description="Remove an existing appointment using the user's phone number.",
)
async def cancel_appointment(body: PhoneRequestBody):
    """
    Cancel appointment using phone number.
    """
    found_id = None
    for app_id, details in appointments.items():
        if details["phone_number"] == body.phone_number:
            found_id = app_id
            break

    if not found_id:
        logger.warning(
            f"Cancel failed: No appointment found for phone {body.phone_number}"
        )
        raise HTTPException(
            status_code=404, detail="No appointment found for this phone number"
        )

    deleted_details = appointments.pop(found_id)
    logger.info(f"Cancelled appointment ID {found_id} for phone: {body.phone_number}")
    return {
        "message": "Appointment cancelled",
        "id": found_id,
        "details": deleted_details,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
