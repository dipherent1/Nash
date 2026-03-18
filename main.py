from fastapi import FastAPI, HTTPException, Body, Depends
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import date, datetime
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
class CheckAvailabilityQuery(BaseModel):
    isEmergency: Optional[bool] = False


class CheckAvailabilityBody(BaseModel):
    target_date: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class CreateClientBody(BaseModel):
    client_first_name: str = Field(..., min_length=1)
    client_last_name: str = Field(..., min_length=1)
    client_phone: str = Field(..., min_length=5)


class BookAppointmentBody(BaseModel):
    client_first_name: str = Field(..., min_length=1)
    client_last_name: str = Field(..., min_length=1)
    client_phone: str = Field(..., min_length=5)
    appointment_datetime: datetime


class CancelAppointmentBody(BaseModel):
    phone: str = Field(..., min_length=5)
    uid: str = Field(..., min_length=3)


ActionType = Literal[
    "checkAvailability",
    "createClient",
    "bookAppointment",
    "cancelAppointment",
]


# Single endpoint with action-based responses
@app.post(
    "/webhook",
    summary="Single endpoint for all actions",
    description="Use query param 'action' to route requests and return different mock responses.",
)
async def webhook(
    action: ActionType,
    query: CheckAvailabilityQuery = Depends(),
    body: Optional[dict] = Body(default=None),
):
    global appointment_counter

    if action == "checkAvailability":
        payload = CheckAvailabilityBody(**(body or {}))
        results = []

        if payload.target_date:
            slot1 = {
                "date": payload.target_date.isoformat(),
                "time": "09:00",
                "available": True,
            }
            slot2 = {
                "date": payload.target_date.isoformat(),
                "time": "14:00",
                "available": True,
            }
            results = [slot1, slot2]
            logger.info(f"Retrieved 2 slots for specific day: {payload.target_date}")
        elif payload.start_date and payload.end_date:
            mid_date = payload.start_date + (payload.end_date - payload.start_date) / 2
            slot = {"date": mid_date.isoformat(), "time": "11:00", "available": True}
            results = [slot]
            logger.info(
                f"Retrieved 1 slot for range: {payload.start_date} to {payload.end_date}"
            )
        else:
            today = date.today()
            results = [{"date": today.isoformat(), "time": "10:00", "available": True}]
            logger.info("Retrieved default slot")

        return {"action": action, "isEmergency": query.isEmergency, "slots": results}

    if action == "createClient":
        payload = CreateClientBody(**(body or {}))
        logger.info(
            f"Created client: {payload.client_first_name} {payload.client_last_name}"
        )
        return {
            "action": action,
            "client": {
                "first_name": payload.client_first_name,
                "last_name": payload.client_last_name,
                "phone": payload.client_phone,
            },
            "status": "created",
        }

    if action == "bookAppointment":
        payload = BookAppointmentBody(**(body or {}))
        new_id = appointment_counter
        appointments[new_id] = {
            "phone_number": payload.client_phone,
            "date": payload.appointment_datetime.date().isoformat(),
            "time": payload.appointment_datetime.time().strftime("%H:%M"),
        }
        appointment_counter += 1
        logger.info(f"Booked appointment ID {new_id} for phone: {payload.client_phone}")
        return {
            "action": action,
            "message": "Appointment booked",
            "uid": f"apt_{new_id}",
            "details": appointments[new_id],
        }

    if action == "cancelAppointment":
        payload = CancelAppointmentBody(**(body or {}))
        found_id = None
        for app_id, details in appointments.items():
            if details["phone_number"] == payload.phone:
                found_id = app_id
                break

        if not found_id:
            logger.warning(
                f"Cancel failed: No appointment found for phone {payload.phone}"
            )
            raise HTTPException(
                status_code=404, detail="No appointment found for this phone number"
            )

        deleted_details = appointments.pop(found_id)
        logger.info(f"Cancelled appointment ID {found_id} for phone: {payload.phone}")
        return {
            "action": action,
            "message": "Appointment cancelled",
            "uid": payload.uid,
            "details": deleted_details,
        }

    raise HTTPException(status_code=400, detail="Unsupported action")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
