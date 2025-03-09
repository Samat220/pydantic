from datetime import datetime
from dateutil.parser import parse
from pydantic import BaseModel, field_validator, ValidationError
from typing import Any


class Model(BaseModel):
    dt: datetime

print(Model(dt="2020-01-01T12:00:00"))
print(Model(dt="2020-01-01T12:00:00Z"))
try:
    Model(dt="2020/1/1 3:00pm")
except ValidationError as ex:
    print(ex)

try:
    Model(dt="Jan 1, 2020 3:00pm")
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")


print(parse("2020/1/1 3pm"))
print(parse("Jan 1, 2020 3pm"))
# can't parse datetime
try:
    parse(datetime(2020, 1, 1, 15, 0, 0))
except TypeError as ex:
    print(ex)

print("\n------------------------------------------\n")

class ModelDateTime(BaseModel):
    dt: datetime

    @field_validator("dt", mode="before")
    @classmethod
    def parse_datetime(cls, value: Any):
        if isinstance(value, str):
            print("parsing string")
            try:
                return parse(value)
            except Exception as ex:
                raise ValueError(str(ex))
        print("pass through...")
        return value

print(ModelDateTime(dt="2020/1/1 3pm"))
print(Model(dt=datetime(2020, 1, 1)))
try:
    Model(dt=[1, 2, 3])
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")


class MultiValidatorModel(BaseModel):
    number: int

    @field_validator("number", mode="before")
    @classmethod
    def validator_1(cls, value):
        print("running validator_1")
        return value

    @field_validator("number", mode="before")
    @classmethod
    def validator_2(cls, value):
        print("running validator_2")
        return value

    @field_validator("number", mode="before")
    @classmethod
    def validator_3(cls, value):
        print("running validator_3")
        return value

print(MultiValidatorModel(number=1))