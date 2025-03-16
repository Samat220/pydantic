from pydantic import BaseModel, Field, ValidationError
from math import pi
from functools import cached_property


class Circle(BaseModel):
    center: tuple[int, int] = (0, 0)
    radius: int = Field(default=1, gt=0)

    def area(self):
        return pi * self.radius ** 2

c = Circle(center=(1, 1), radius=2)

print(c.model_dump())
print(c.area())

print("\n------------------------------------------\n")


class Circle2(BaseModel):
    center: tuple[int, int] = (0, 0)
    radius: int = Field(default=1, gt=0)

    @property
    def area(self):
        return pi * self.radius ** 2

m = Circle2()
print(m.area)
print(m.model_dump())
print(m.model_dump_json())
print(m.model_fields)

print("\n------------------------------------------\n")

class Circle3(BaseModel):
    center: tuple[int, int] = (0, 0)
    radius: int = Field(default=1, gt=0, frozen=True)

    @cached_property
    def area(self):
        print("calculating area...")
        return pi * self.radius ** 2

c3 = Circle3()
print(c3)
print(c3.area)

try:
    c3.radius=2
except ValidationError as ex:
    print(ex)
