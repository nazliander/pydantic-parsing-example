
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl
from enum import Enum


class MessageTypeAbbreviationEnum(str, Enum):
    FLR = "FLR"
    SEP = "SEP"
    CME = "CME"
    IPS = "IPS"
    MPC = "MPC"
    GST = "GST"
    RBE = "RBE"
    Report = "Report"


class NotificationMessageBody(BaseModel):
    message_type: str
    message_issue_date: datetime
    message_id: str
    disclaimer: Optional[str]
    summary: Optional[str]
    notes: Optional[str]


class NotificationMessage(BaseModel):
    insertion_date: datetime
    message_type_abbreviation: MessageTypeAbbreviationEnum
    message_url: HttpUrl
    message_body: NotificationMessageBody

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }
