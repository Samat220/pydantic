from pydantic import BaseModel, PositiveInt, ValidationError


class Circle(BaseModel):
    center: tuple[int, int] = (0, 0)
    radius: PositiveInt = 1

try:
    Circle(center=(0.5, 0.5), radius = 0)  # fails due to radius positive int restriction and int requirement
except ValidationError as ex:
    print(ex)

print("\n------------------------------------------")

print(Circle.model_fields)