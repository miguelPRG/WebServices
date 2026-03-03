from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class ReservationCreate(BaseModel):
    user_id: str = Field(..., regex='^[0-9a-fA-F]{24}$')
    room_id: str = Field(..., regex='^[0-9a-fA-F]{24}$')
    start_datetime: datetime
    end_datetime: datetime
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        valid_statuses = {"livre", "ocupado"}
        if value not in valid_statuses:
            raise ValueError(f"Status inválido. Deve ser um dos seguintes: {', '.join(valid_statuses)}")
        return value