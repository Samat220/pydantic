from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime
import pytz

class BasicModel(BaseModel):
    number: int = Field(gt=0, lt=10)

print(BasicModel(number="4"))

try:
    BasicModel(number=12)
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")

class BasicModel1(BaseModel):
    number: int = Field(gt=0, lt=10)

    @field_validator("number")
    @classmethod
    def validate_even(cls, value):
        print("Running custom validator")
        print(f"{value=}, {type(value)=}")
        return value  # custom validators must return a value

print(BasicModel1(number=3))
print(BasicModel1(number="3"))
try:
    BasicModel1(number=12)
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")


class ValueErrorModel(BaseModel):
    number: int = Field(gt=0, lt=10)

    @field_validator("number")
    @classmethod
    def validate_even(cls, value):
        print("Running custom validator")
        print(f"{value=}, {type(value)=}")
        if value % 2 == 0:
            # number is even, so return it
            return value
        raise ValueError("value must be even")

print(ValueErrorModel(number=4))

try:
    ValueErrorModel(number=3)
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")

class TypeErrorModel(BaseModel):
    number: int = Field(gt=0, lt=10)

    @field_validator("number")
    @classmethod
    def validate_even(cls, value):
        print("Running custom validator")
        print(f"{value=}, {type(value)=}")
        if value % 2 == 0:
            # number is even, so return it
            return value
        raise TypeError("value must be even")

try:
    TypeErrorModel(number=3)
except Exception as ex:
    print(f"{type(ex)=}, {ex}")


print("\n------------------------------------------\n")


class Model(BaseModel):
    even: int

    @field_validator("even")
    @classmethod
    def make_even(cls, value: int) -> int:
        if value % 2 == 1:
            return value + 1
        return value


print(Model(even=3))
print("\n------------------------------------------\n")


# def make_utc(dt: datetime) -> datetime:
#     if dt.tzinfo is None:
#         dt = pytz.utc.localize(dt)
#     else:
#         dt = dt.astimezone(pytz.utc)
#     return dt


class ModelUTC(BaseModel):
    dt: datetime

    @field_validator("dt")
    @classmethod
    def make_utc(cls, dt: datetime) -> datetime:
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        else:
            dt = dt.astimezone(pytz.utc)
        return dt


print(ModelUTC(dt="2020-01-01T03:00:00"))

eastern = pytz.timezone('US/Eastern')
dt = eastern.localize(datetime(2020, 1, 1, 3, 0, 0))
print(ModelUTC(dt=dt))

print("\n------------------------------------------\n")

class MultiValidatorModel(BaseModel):
    number: int

    @field_validator("number")
    @classmethod
    def add_1(cls, value: int):
        print(f"running add_1({value}) -> {value + 1}")
        return value + 1

    @field_validator("number")
    @classmethod
    def add_2(cls, value: int):
        print(f"running add_2({value}) -> {value + 2}")
        return value + 2

    @field_validator("number")
    @classmethod
    def add_3(cls, value: int):
        print(f"running add_3({value}) -> {value + 3}")
        return value + 3

print(MultiValidatorModel(number=1))

print("\n------------------------------------------\n")

# Applying validator to multiple fields
class Model1(BaseModel):
    unit_cost: float
    unit_price: float

    @field_validator("unit_cost", "unit_price")
    @classmethod
    def round_2(cls, value: float) -> float:
        return round(value, 2)

print(Model1(unit_cost=2.12345, unit_price=5.9876))

print("\n------------------------------------------\n")

class Model2(BaseModel):
    unit_cost: float
    unit_price: float

    @field_validator("*")
    @classmethod
    def round_2(cls, value: float) -> float:
        return round(value, 2)

print(Model2(unit_cost=2.12345, unit_price=5.9876))
