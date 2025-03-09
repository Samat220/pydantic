from pydantic import BaseModel, field_validator, ValidationError, ValidationInfo
from datetime import datetime
from typing import Annotated, Any

import pytz
from dateutil.parser import parse
from pydantic import AfterValidator, BeforeValidator


class Model(BaseModel):
    field_1: int
    field_2: list[int]
    field_3: str
    field_4: list[str]

    @field_validator("field_3")
    @classmethod
    def validator(cls, value: str, validated_values: ValidationInfo):
        print(f"{value=}")
        print(f"{validated_values=}")
        return value

print(Model(field_1=100, field_2=[1, 2, 3], field_3="python", field_4=["a", "b"]))


try:
    Model(field_1=100, field_2=["a", "b"], field_3="python", field_4=["a", "b"])
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")


def parse_datetime(value: Any):
    if isinstance(value, str):
        try:
            return parse(value)
        except Exception as ex:
            raise ValueError(str(ex))
    return value


def make_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    else:
        dt = dt.astimezone(pytz.utc)
    return dt

DateTimeUTC = Annotated[datetime, BeforeValidator(parse_datetime), AfterValidator(make_utc)]

class ModelDate(BaseModel):
    start_dt: DateTimeUTC
    end_dt: DateTimeUTC

    @field_validator("end_dt")
    @classmethod
    def validate_end_after_start_dt(cls, value: datetime, values: ValidationInfo):
        data = values.data
        if "start_dt" in data:
            if value <= data["start_dt"]:
                raise ValueError("end_dt must come after start_dt")
        # if start_dt failed validation, there's not much we can check here.
        #    So just return value as-is
        return value

print(ModelDate(start_dt="2020/1/1", end_dt="2020/12/31"))

try:
    ModelDate(start_dt="2020/1/1", end_dt="2012/12/31")
except ValidationError as ex:
    print(ex)