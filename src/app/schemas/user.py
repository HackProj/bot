import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SomeData(BaseModel):
    data : str