from pprint import pprint
from typing import Annotated
from typing import get_args
from pydantic import BaseModel, Field


SpecialInt = Annotated[int, "metadata 1", [1, 2, 3], 100]

print(get_args(SpecialInt))

class Model(BaseModel):
    x: int = Field(gt=0, le=100)
    y: int = Field(gt=0, le=100)
    z: int = Field(gt=0, le=100)

pprint(Model.model_fields)

BoundedInt = Annotated[int, Field(gt=0, le=100)]

class Model1(BaseModel):
    x: BoundedInt
    y: BoundedInt
    z: BoundedInt

pprint(Model1.model_fields)
print(Model1(x=10, y=20, z=30))

try:
    Model(x=0, y=10, z=103)
except ValueError as ex:
    print(ex)

print("\n------------------------------------------\n")

class Model2(BaseModel):
    field_1: Annotated[int, Field(gt=0)] = 1
    field_2: Annotated[str, Field(min_length=1, max_length=10)] | None = None

try:
    Model2(field_1=-10, field_2 = "Python" * 3)
except ValueError as ex:
    print(ex)