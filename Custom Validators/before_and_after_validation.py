from datetime import datetime
from typing import Any

import pytz
from dateutil.parser import parse
from pydantic import BaseModel, field_validator, ValidationError


class ModelBefore(BaseModel):
    dt: datetime

    @field_validator("dt", mode="before")
    @classmethod
    def parse_datetime(cls, value: Any):
        if isinstance(value, str):
            try:
                return parse(value)
            except Exception as ex:
                raise ValueError(str(ex))
        return value

print(ModelBefore(dt=100_000))
print(ModelBefore(dt="2020/1/1 3pm"))

print("\n------------------------------------------\n")

class ModelAfter(BaseModel):
    dt: datetime

    @field_validator("dt")
    @classmethod
    def make_utc(cls, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        else:
            dt = dt.astimezone(pytz.utc)
        return dt

class Combined(BaseModel):
    dt: datetime

    @field_validator("dt", mode="before")
    @classmethod
    def parse_datetime(cls, value: Any):
        if isinstance(value, str):
            try:
                return parse(value)
            except Exception as ex:
                raise ValueError(str(ex))
        return value

    @field_validator("dt")
    @classmethod
    def make_utc(cls, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        else:
            dt = dt.astimezone(pytz.utc)
        return dt

print(Combined(dt=100_000))
print(Combined(dt="2020/1/1 3pm"))

eastern = pytz.timezone('US/Eastern')

print(Combined(dt=eastern.localize(datetime(2020, 1, 1, 3, 0, 0))))


print("\n------------------------------------------\n")

class Model(BaseModel):
    number: int

    @field_validator("number")
    @classmethod
    def after_validator_1(cls, value):
        print("after_validator_1")
        return value

    @field_validator("number")
    @classmethod
    def after_validator_2(cls, value):
        print("after_validator_2")
        return value

    @field_validator("number", mode="before")
    @classmethod
    def before_validator_1(cls, value):
        print("before_validator_1")
        return value

    @field_validator("number")
    @classmethod
    def after_validator_3(cls, value):
        print("after_validator_3")
        return value

    @field_validator("number", mode="before")
    @classmethod
    def before_validator_2(cls, value):
        print("before_validator_2")
        return value

print(Model(number=10))