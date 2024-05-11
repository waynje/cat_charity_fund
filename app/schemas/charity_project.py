from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

MIN_FIELD_LENGTH = 1
MAX_FIELD_LENGTH = 100


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None,
                                min_length=MIN_FIELD_LENGTH,
                                max_length=MAX_FIELD_LENGTH)
    description: Optional[str] = Field(None,
                                       min_length=MIN_FIELD_LENGTH)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(...,
                      min_length=MIN_FIELD_LENGTH,
                      max_length=MAX_FIELD_LENGTH)
    description: str = Field(...,
                             min_length=MIN_FIELD_LENGTH)
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True