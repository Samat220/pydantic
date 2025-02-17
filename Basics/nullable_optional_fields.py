from pydantic import BaseModel, ValidationError


print("\n1. Required, non nullable field")
class Model(BaseModel):
    field: int

try:
    Model()
except ValidationError as ex:
    print(ex)


print("\n2. Required, nullable field")
class Model2(BaseModel):
    field: int | None

try:
    Model2()
except ValidationError as ex:
    print(ex)

print("\n3. Optional, Not nullable field")
class Model3(BaseModel):
    field: int = 0  # make sure default is consistent with the type of the field


try:
    Model3(field = None)
except ValidationError as ex:
    print(ex)


print("\n4. Optional, Nullable field")
class Model4(BaseModel):
    field: int | None = 0


try:
    Model4(field = None)
except ValidationError as ex:
    print(ex)