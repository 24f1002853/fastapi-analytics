from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL = "24f1002853@ds.study.iitm.ac.in"
API_KEY = "ak_ry4mt5tw9jbo4gt3sqal4cw2"


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: List[Event]


@app.post("/analytics")
async def analytics(
    payload: AnalyticsRequest,
    x_api_key: str = Header(None, alias="X-API-Key")
):

    if x_api_key != API_KEY:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized"},
        )

    total_events = len(payload.events)

    unique_users = len({e.user for e in payload.events})

    revenue = 0.0
    user_totals = {}

    for event in payload.events:

        if event.amount > 0:

            revenue += event.amount

            user_totals[event.user] = (
                user_totals.get(event.user, 0) + event.amount
            )

    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }
