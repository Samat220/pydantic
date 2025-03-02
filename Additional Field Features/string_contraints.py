from pydantic import BaseModel, Field, ValidationError

class Model(BaseModel):
    name: str = Field(min_length=1, max_length=20)

try:
    Model(name="")
except ValidationError as ex:
    print(ex)
print("\n------------------------------------------\n")

try:
    Model(name="*" * 21)
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")


class Model1(BaseModel):
    items: list[float] = Field(min_length=3, max_length=5, default=[1.0, 2.0, 3.0])

print(Model1())
print(Model1(items=[2, 3.5, 4]))

try:
    Model(items=[1, 2])
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")
class Circle(BaseModel):
    center: tuple[int]
    radius: int = Field(gt=0, default=1)

try:
    Circle(center=(1, 1), radius=1)
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")
class Circle1(BaseModel):
    center: tuple[int, ...]
    radius: int = Field(gt=0, default=1)

print(Circle1(center=(1, 2, 3, 4, 5)))

print("\n------------------------------------------\n")
class Circle2(BaseModel):
    center: tuple[int, ...] = Field(min_length=2, max_length=3, default=(0, 0))
    radius: int = Field(gt=0, default=1)

try:
    Circle2(center=(1, ))
except ValidationError as ex:
    print(ex)

try:
    Circle2(center=(1, 2, 3, 4))
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------\n")

class Address(BaseModel):
    zip_code: str = Field(pattern=r"^[0-9]{5}(?:-[0-9]{4})?$")

print(Address(zip_code="12345"))

try:
    Address(zip_code="12345-12345")
except ValidationError as ex:
    print(ex)