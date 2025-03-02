from pydantic import BaseModel, PositiveInt, ValidationError, conlist, PydanticUserError

class Circle(BaseModel):
    center: tuple[int, int] = (0, 0)
    radius: PositiveInt = 1

class Sphere(BaseModel):
    center: tuple[int, int] | tuple[int, int, int] = (0, 0)
    radius: PositiveInt = 1

sphere_2d = Sphere(center=(1, 1), radius=10)
print(sphere_2d)

sphere_3d = Sphere(center=(1, 2, 3), radius=5)
print(sphere_3d)

print("\n------------------------------------------")

try:
    Sphere(center=(1, 2, 3, 4))
except ValidationError as ex:
    print(ex)


print("\n------------------------------------------")
class Sphere(BaseModel):
    center: conlist(int, min_length=2, max_length=3) = [0, 0]
    radius: PositiveInt = 1



try:
    Sphere(center=(1, 2, 3, 4))
except ValidationError as ex:
    print(ex)
print("\n------------------------------------------")


try:
    Sphere(center=(1, ))
except ValidationError as ex:
    print(ex)


print("\n------------------------------------------")

try:
    class Model(BaseModel):
        unique_elements: conlist(int, min_length=1, max_length=10, unique_items=True)  # deprecated
except PydanticUserError as ex:# use set
    print(ex)