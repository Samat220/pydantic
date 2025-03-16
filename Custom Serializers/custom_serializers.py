from datetime import datetime
from typing import Annotated, Any
import pytz
from dateutil.parser import parse
from pydantic import BaseModel, AfterValidator, BeforeValidator, PlainSerializer, field_serializer


def make_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    else:
        dt = dt.astimezone(pytz.utc)
    return dt


def parse_datetime(value: Any):
    if isinstance(value, str):
        try:
            return parse(value)
        except Exception as ex:
            raise ValueError(str(ex))
    return value


DateTimeUTC = Annotated[datetime, BeforeValidator(parse_datetime), AfterValidator(make_utc)]


def dt_json_serializer(dt: datetime) -> str:
    return dt.strftime("%Y/%m/%d %I:%M %p UTC")

class Model(BaseModel):
    dt: DateTimeUTC

    @field_serializer("dt", when_used="json-unless-none")
    def serialize_dt_to_json(self, value: datetime) -> str:
        return dt_json_serializer(value)

m = Model(dt="2020/1/1 3pm")
print(m)
print(m.model_dump())
print(m.model_dump_json())

print("\n------------------------------------------\n")

DateTimeUTC2 = Annotated[
    datetime,
    BeforeValidator(parse_datetime),
    AfterValidator(make_utc),
    PlainSerializer(dt_json_serializer, when_used="json-unless-none"),
]

class Model2(BaseModel):
    dt: DateTimeUTC2

m2 = Model(dt="2020/1/1 3pm")
print(m2)
print(m2.model_dump())
print(m2.model_dump_json())