from pydantic import BaseModel, Field, ValidationError
from typing import Annotated
from datetime import datetime
from typing import Any
from pydantic import BeforeValidator, AfterValidator
from dateutil.parser import parse
import pytz

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

# Use annotated types with before validators
DateTime = Annotated[datetime, BeforeValidator(parse_datetime)]

class ModelDate(BaseModel):
    dt: DateTime

print(ModelDate(dt="2020/1/1 3pm"))

DateTimeUTC = Annotated[datetime, BeforeValidator(parse_datetime), AfterValidator(make_utc)]
print("\n------------------------------------------\n")

class ModelDateTime(BaseModel):
    dt: DateTime

print(ModelDateTime(dt="2020/1/1 3pm"))

eastern = pytz.timezone('US/Eastern')
dt = eastern.localize(datetime(2020, 1, 1, 3, 0, 0))

print(ModelDateTime(dt=dt))

print("\n------------------------------------------\n")

def before_validator_1(value):
    print("before_validator_1")
    return value


def before_validator_2(value):
    print("before_validator_2")
    return value


def before_validator_3(value):
    print("before_validator_3")
    return value


def after_validator_1(value):
    print("after_validator_1")
    return value


def after_validator_2(value):
    print("after_validator_2")
    return value


def after_validator_3(value):
    print("after_validator_3")
    return value

CustomType = Annotated[
    int,
    BeforeValidator(before_validator_1),
    AfterValidator(after_validator_1),
    BeforeValidator(before_validator_2),
    AfterValidator(after_validator_2),
    AfterValidator(after_validator_3),
    BeforeValidator(before_validator_3),
]


class ModelCombined(BaseModel):
    number: CustomType


print(ModelCombined(number=10))

print("\n------------------------------------------\n")

def are_elements_unique(values: list[Any]) -> list[Any]:
    unique_elements = []
    for value in values:
        if value in unique_elements:
            raise ValueError("elements must be unique")
        unique_elements.append(value)
    return values


UniqueIntegerList = Annotated[list[int], AfterValidator(are_elements_unique)]

class UniqueModel(BaseModel):
    numbers: UniqueIntegerList = []

m = UniqueModel(numbers=(1, 2, 3, 4, 5))
print(m)

try:
    UniqueModel(numbers=[1, 1, 2, 3])
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")

from typing import TypeVar
T = TypeVar('T')

UniqueList = Annotated[list[T], AfterValidator(are_elements_unique)]

class ModelUniqueList(BaseModel):
    numbers: UniqueList[int] = []
    strings: UniqueList[str] = []


print(ModelUniqueList(numbers=[1, 2, 3], strings=["pyt", "hon"]))
try:
    ModelUniqueList(numbers=[1, 1, 2])
except ValidationError as ex:
    print(ex)

try:
    ModelUniqueList(numbers=["a", 2, 3], strings=[1, "b"])
except ValidationError as ex:
    print(ex)


UniqueList2 = Annotated[
    list[T],
    Field(min_length=1, max_length=5),
    AfterValidator(are_elements_unique)
]

class ModelUniqueList2(BaseModel):
    numbers: UniqueList2[int] = []
    strings: UniqueList2[str] = []

print(ModelUniqueList2(numbers=[1, 2, 3], strings=["a", "b", "c"]))

try:
    ModelUniqueList2(numbers=[], strings=list("python"))
except ValidationError as ex:
    print(ex)

print(ModelUniqueList2())  # bug in validation -> []