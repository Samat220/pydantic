from functools import cached_property
from math import pi
from pydantic import BaseModel, computed_field, Field, PydanticUserError, ValidationError

class Circle(BaseModel):
    center: tuple[int, int] = (0, 0)
    radius: int = Field(default=1, gt=0, frozen=True)

    @computed_field(alias="AREA", repr=False)
    @cached_property
    def area(self) -> float:
        print("calculating area...")
        return pi * self.radius ** 2

c = Circle()
print(c.area)
print(c.area)
