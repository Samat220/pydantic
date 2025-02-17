from pydantic import BaseModel, ValidationError

class Model(BaseModel):
    field: int  # required object

try:
    Model(field=None)  # this will say that its of wrong type
except ValidationError as ex:
    print(ex)

try:
    Model()  # this will say that its missing required field
except ValidationError as ex:
    print(ex)

print("------------------------------------------")
print("Model")
class Model2(BaseModel):
    field: int | None

try:
    Model2(field=None)  # this is fine as it is nullable
except ValidationError as ex:
    print(ex)

try:
    Model2()  # this will say that its missing required field
except ValidationError as ex:
    print(ex)

# Using Union
from typing import Union

class UnionModel(BaseModel):
    field: Union[int, None]  # canonical way to define nullable
print("------------------------------------------")
print("UnionModel")
try:
    UnionModel()  # this will say that its missing required field
except ValidationError as ex:
    print(ex)

# Using optional
from typing import Optional

class OptionalModel(BaseModel):
    field: Optional[int] # nullable but not actually optional

print("------------------------------------------")
print("OptionalModel")

try:
    OptionalModel()  # this will say that its missing required field
except ValidationError as ex:
    print(ex)


print("------------------------------------------")
print("New Model")

class Model(BaseModel):
    field_1: int | None
    field_2: Union[int, None]
    field_3: Optional[int]

print(Model.model_fields)