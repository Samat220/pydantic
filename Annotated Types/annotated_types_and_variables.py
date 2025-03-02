from typing import Annotated
from typing import Any
from pydantic import BaseModel, Field, ValidationError
from typing import TypeVar

class Model(BaseModel):
    elements: list[int] = Field(default=[], max_length=10)

m = Model(elements=[1, 2, 3])
print(m)

try:
    Model(elements = [1, ] * 20)
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")

BoundedListInt = Annotated[list[int], Field(max_length=10)]

class Model2(BaseModel):
    field_1: BoundedListInt = []
    field_2: BoundedListInt = []

BoundedListFloat = Annotated[list[float], Field(max_length=10)]
BoundedListString = Annotated[list[str], Field(max_length=10)]
# BoundedList = Annotated[list[Any], Field(max_length=10)]

T = TypeVar('T')
BoundedList = Annotated[list[T], Field(max_length=10)]

class Model1(BaseModel):
    integers: BoundedList[int] = []
    strings: BoundedList[str] = []

print(Model1(integers=[1.0, 2.0], strings=["abc", "def"]))
try:
    Model1(integers=[0.5])
except ValidationError as ex:
    print(ex)