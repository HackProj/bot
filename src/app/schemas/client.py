import datetime
import re

from pydantic import BaseModel, ValidationError, validator


class ClientFullData(BaseModel):
    id: int
    login: str
    is_active: bool


class CreateClientRequest(BaseModel):
    login: str


class ClientQuestionnaireData(ClientFullData):
    height: float
    weight: float
    diabet: bool
    card: bool
