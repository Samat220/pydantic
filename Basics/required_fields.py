from pydantic import BaseModel, ValidationError

class Circle(BaseModel):
    center: tuple[int, int] = (0, 0) # center is optional here
    radius: int


circle = Circle(radius=2)

data = {"radius": 1}
data_json = '{"radius": 1}'

Circle.model_validate(data)

Circle.model_validate_json(data_json)

class Model(BaseModel):
    field: int = "Python" # default has to be of correct type, but it is not validated here

class Model2(BaseModel):
    field: int[] = [] # this is perfectly fine
